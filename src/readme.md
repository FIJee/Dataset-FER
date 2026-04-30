## 📸 Panduan Pengujian Sistem (Camera & System Test)

Bagian ini menjelaskan langkah-langkah untuk melakukan pengujian fungsionalitas kamera dan integrasi model AI pada perangkat Anda.

### 1. Tahap Persiapan Lingkungan
Sebelum menjalankan pengujian, pastikan langkah-langkah dasar berikut telah terpenuhi:
* **Instalasi Dependensi:** Pastikan seluruh pustaka dalam file `requirements.txt` telah terinstal dengan sempurna melalui perintah `pip install -r requirements.txt`.
* **Penempatan Model:** File `model_ekspresi.tflite` wajib berada di dalam folder bernama `models` yang terletak di satu direktori yang sama dengan file skrip utama. Sistem tidak akan berjalan jika path model tidak ditemukan.

### 2. Konfigurasi Perangkat Kamera
Sistem dirancang untuk mendeteksi perangkat input video secara otomatis:
* **Deteksi Otomatis:** Program akan mencari perangkat video pada indeks 0 (Webcam bawaan laptop atau kamera pertama yang terdeteksi di Raspberry Pi).
* **Koneksi USB:** Jika menggunakan webcam eksternal, pastikan kabel USB terpasang dengan kuat sebelum menjalankan skrip. 
* **Izin Akses:** Pada beberapa sistem operasi (seperti macOS atau Windows 11), pastikan Anda telah memberikan izin bagi Terminal atau Python untuk mengakses kamera.

### 3. Langkah Menjalankan Tes
Buka terminal/command prompt, masuk ke folder proyek, lalu ketik perintah:
`python nama_file_program.py`

Setelah perintah dijalankan, sistem akan melakukan inisialisasi:
1. **Loading Model:** AI akan memuat model TFLite ke dalam memori.
2. **Camera Warm-up:** Lampu indikator kamera akan menyala dan jendela baru bertajuk "Monitoring Pelayanan" akan muncul di layar.

### 4. Prosedur Pengujian Fungsional
Lakukan pengujian berikut untuk memastikan sistem bekerja sesuai parameter:
* **Tes Area Wajah:** Pastikan wajah berada di area tengah frame. Sistem harus menampilkan kotak pembatas (bounding box) dan teks status ekspresi (Senyum/Netral/Cemberut).
* **Tes Gestur Tangan:** Angkat tangan Anda ke depan kamera. Lakukan gestur salam atau tangan di dada. Sistem harus memperbarui status gestur secara responsif.
* **Tes Logika Fuzzy:** Perhatikan apakah nilai "Skor Pelayanan" berubah secara dinamis setiap kali Anda mengubah ekspresi atau gestur tangan.
* **Tes Stabilitas:** Pastikan tidak ada kendala *freeze* pada gambar. Jika gambar tersendat, periksa beban CPU pada perangkat Anda.

### 5. Menghentikan Sistem
Untuk menutup akses kamera dan memberhentikan program secara bersih (*clean exit*), tekan tombol **ESC** pada keyboard. Jangan menutup jendela kamera secara paksa melalui tombol silang (X) pada jendela agar proses kamera tidak tertahan di latar belakang (background process).

---

### Tips Optimasi Pengujian:
* **Pencahayaan:** Lakukan pengujian di ruangan dengan cahaya yang cukup. Cahaya latar (backlight) yang terlalu kuat dapat mengganggu akurasi deteksi wajah.
* **Jarak Pandang:** Jarak ideal antara kamera dan pengguna adalah sekitar 50cm hingga 1 meter untuk memastikan titik kunci (keypoints) wajah dan tangan terdeteksi dengan detail.
