import cv2
import numpy as np
import tensorflow as tf 
import mediapipe as mp
import threading

# ==========================================
# 1. OPTIMASI KAMERA (THREADING)
# ==========================================
class WebcamStream:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        threading.Thread(target=self.update, args=(), daemon=True).start()
        return self

    def update(self):
        while True:
            if self.stopped: return
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True
        self.stream.release()

# ==========================================
# 2. SETUP MODEL & MEDIAPIPE
# ==========================================
interpreter = tf.lite.Interpreter(model_path="model_ekspresi.tflite", num_threads=4)
interpreter.allocate_tensors()
input_details, output_details = interpreter.get_input_details(), interpreter.get_output_details()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, model_complexity=0)
mp_face = mp.solutions.face_detection
face_detection = mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.5)

# ==========================================
# 3. MAIN PROGRAM
# ==========================================
vs = WebcamStream(src=0).start()
count = 0

# Variabel Monitoring (State)
score_ekspresi = 0.5
status_ekspresi = "Netral"
score_gestur = 0.5
status_gestur = "Standby"

while True:
    frame = vs.read()
    if frame is None: break
    
    count += 1
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # --- A. LOGIKA GESTUR (UPDATING VERSI TERBAIK) ---
    if count % 2 == 0:
        hand_results = hands.process(rgb)
        if hand_results.multi_hand_landmarks:
            num_hands = len(hand_results.multi_hand_landmarks)
            
            # 1. Salam (2 Tangan Rapat)
            if num_hands == 2:
                w1, w2 = hand_results.multi_hand_landmarks[0].landmark[0], hand_results.multi_hand_landmarks[1].landmark[0]
                if abs(w1.x - w2.x) < 0.15:
                    status_gestur, score_gestur = "BAIK (Salam)", 0.95
            
            # 2. Deteksi Jari & Posisi
            else:
                for hl in hand_results.multi_hand_landmarks:
                    fingers = []
                    for tip, pip in zip([8, 12, 16, 20], [6, 10, 14, 18]):
                        fingers.append(1 if hl.landmark[tip].y < hl.landmark[pip].y else 0)
                    
                    up_fingers = sum(fingers)
                    wrist_y = hl.landmark[0].y

                    # Perbaikan: Cek Genggam Terlebih Dahulu
                    if up_fingers == 0: 
                        status_gestur, score_gestur = "BURUK (Mengepal)", 0.15
                    elif 0.3 < wrist_y < 0.7 and up_fingers >= 3:
                        status_gestur, score_gestur = "BAIK (Tangan di Dada)", 0.90
                    elif fingers == [1, 0, 0, 0]:
                        status_gestur, score_gestur = "BURUK (Tunjuk Kasar)", 0.20
                    elif up_fingers >= 3:
                        status_gestur, score_gestur = "NETRAL (Sopan)", 0.60
        else:
            status_gestur, score_gestur = "Tangan Tidak Terlihat", 0.30

    # --- B. LOGIKA EKSPRESI (LOCKED - VERSI PALING BAGUS) ---
    if count % 3 == 0:
        face_results = face_detection.process(rgb)
        if face_results.detections:
            for detection in face_results.detections:
                bbox = detection.location_data.relative_bounding_box
                x, y, bw, bh = int(bbox.xmin*w), int(bbox.ymin*h), int(bbox.width*w), int(bbox.height*h)
                x, y, x2, y2 = max(0, x), max(0, y), min(w, x+bw), min(h, y+bh)

                face_img = frame[y:y2, x:x2]
                if face_img.size > 0:
                    face_resized = cv2.resize(face_img, (224, 224))
                    face_input = np.expand_dims(face_resized.astype('float32') / 255.0, axis=0)

                    interpreter.set_tensor(input_details[0]['index'], face_input)
                    interpreter.invoke()
                    preds = interpreter.get_tensor(output_details[0]['index'])[0]
                    
                    c_conf, n_conf, s_conf = preds[0], preds[1], preds[2]
                    
                    if s_conf > n_conf and s_conf > c_conf:
                        status_ekspresi = "Senyum 2 (Lebar)" if s_conf > 0.85 else "Senyum 1 (Tipis)"
                        score_ekspresi = 0.95 if s_conf > 0.85 else 0.75
                    elif c_conf > n_conf and c_conf > s_conf:
                        status_ekspresi = "Cemberut 2 (Marah)" if c_conf > 0.85 else "Cemberut 1"
                        score_ekspresi = 0.10 if c_conf > 0.85 else 0.30
                    else:
                        status_ekspresi, score_ekspresi = "Netral", 0.50

    # --- C. UI DISPLAY ---
    cv2.rectangle(frame, (0,0), (350, 140), (0,0,0), -1)
    cg = (0,255,0) if score_gestur > 0.7 else (0,0,255) if score_gestur < 0.4 else (255,255,0)
    ce = (0,255,0) if score_ekspresi > 0.6 else (0,0,255) if score_ekspresi < 0.4 else (255,255,255)

    cv2.putText(frame, f"G: {status_gestur}", (10, 30), 1, 1.2, cg, 2)
    cv2.putText(frame, f"Score G: {score_gestur}", (10, 60), 1, 1.0, cg, 1)
    cv2.putText(frame, f"E: {status_ekspresi}", (10, 100), 1, 1.2, ce, 2)
    cv2.putText(frame, f"Score E: {score_ekspresi:.2f}", (10, 125), 1, 1.0, ce, 1)

    cv2.imshow("Monitoring Pelayanan", frame)
    if cv2.waitKey(1) & 0xFF == 27: break

vs.stop()
cv2.destroyAllWindows()
