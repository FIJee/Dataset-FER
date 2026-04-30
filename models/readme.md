## 📂 Penjelasan Model AI (`models/`)

Di dalam folder ini terdapat dua jenis format model yang digunakan dalam siklus pengembangan sistem ini. Transisi dari format `.h5` ke `.tflite` merupakan langkah krusial untuk implementasi pada perangkat keras.

### 1. Perbedaan Format Model

| Karakteristik | Model Keras (`.h5`) | Model TensorFlow Lite (`.tflite`) |
| :--- | :--- | :--- |
| **Fase** | Pengembangan & Pelatihan (*Training*) | Implementasi (*Deployment*) |
| **Ukuran File** | Lebih Besar | Terkompresi & Ringan |
| **Presisi** | Float32 (Sangat Detail) | Dioptimalkan untuk kecepatan |
| **Target Perangkat** | PC / Server (Powerful GPU/CPU) | Raspberry Pi / Perangkat *Embedded* |

### 2. Mengapa Menggunakan TFLite?

Pemilihan format **TensorFlow Lite** dibandingkan format standar `.h5` didasari oleh keterbatasan sumber daya pada Raspberry Pi. Berikut adalah alasan utamanya:

* **Efisiensi Sumber Daya:** Perangkat Raspberry Pi memiliki RAM dan CPU yang terbatas. TFLite dirancang untuk menggunakan memori seminimal mungkin agar sistem tidak mengalami *crash*.
* **Kecepatan Inferensi (Real-time):** TFLite menggunakan *interpreter* yang dioptimalkan untuk arsitektur prosesor ARM. Hal ini memungkinkan deteksi ekspresi wajah berjalan dengan FPS (Frame Per Second) yang lebih tinggi dan tanpa *delay*.
* **Optimasi Multi-core:** Implementasi TFLite dalam proyek ini memanfaatkan fitur `num_threads`, sehingga beban kerja AI dibagi rata ke seluruh *core* CPU Raspberry Pi, yang meningkatkan stabilitas sistem secara keseluruhan.
* **Pengurangan Ukuran Model:** Konversi ke TFLite membuang metadata yang tidak diperlukan untuk deteksi (seperti konfigurasi *optimizer*), sehingga model lebih fokus pada eksekusi prediksi saja.

---

### Cara Menggunakan Model

Untuk menjalankan inferensi menggunakan model TFLite di Raspberry Pi, sistem menggunakan `Interpreter` dari pustaka `tflite-runtime`:

```python
# Contoh inisialisasi model di perangkat edge
from tflite_runtime.interpreter import Interpreter

interpreter = Interpreter(model_path="models/model_ekspresi.tflite")
interpreter.allocate_tensors()
