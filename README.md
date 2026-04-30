# Dataset-FER
## 🛠️ Persyaratan Sistem (Requirements)

Proyek ini memerlukan Python versi **3.9 - 3.11**. Pustaka yang digunakan dibagi menjadi beberapa fungsi utama:

### 🔹 Pemrosesan Citra & AI
* **OpenCV & MediaPipe**: Digunakan untuk menangkap *stream* kamera dan mendeteksi titik koordinat wajah serta tangan secara *real-time*.
* **TFLite-Runtime**: Interpreter khusus yang dioptimalkan untuk menjalankan model `.tflite` pada perangkat dengan sumber daya terbatas (Raspberry Pi).

### 🔹 Logika Pengambil Keputusan
* **Scikit-Fuzzy**: Digunakan untuk mengimplementasikan algoritma **Fuzzy Logic Mamdani** yang mengonversi skor ekspresi dan gestur menjadi nilai kualitas pelayanan.

### 🔹 Analisis Data & Training
* **TensorFlow & Scikit-Learn**: Digunakan selama fase pelatihan model MobileNetV2 dan evaluasi statistik (akurasi, presisi, recall).
