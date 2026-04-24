## 📊 Struktur Dataset & Penyederhanaan Kelas

Untuk meningkatkan akurasi dan efisiensi model pada perangkat *edge* (Raspberry Pi), beberapa variasi ekspresi yang serupa digabungkan ke dalam tiga kelas utama.

### 1. Tabel Pembagian Data
Berikut adalah rincian jumlah data setelah proses penyederhanaan kelas:

| Ekspresi Awal (Input) | Label Model Akhir | Data Train | Data Val | Data Test | Total |
| :--- | :--- | :---: | :---: | :---: | :---: |
| Senyum Sedang | **Senyum** | 900 | 60 | 60 | 1020 |
| Senyum Lebar | **Senyum** | (Gabung) | (Gabung) | (Gabung) | - |
| Netral | **Netral** | 900 | 60 | 60 | 1020 |
| Cemberut Sedang | **Cemberut** | 900 | 60 | 60 | 1020 |
| Cemberut Berlebihan | **Cemberut** | (Gabung) | (Gabung) | (Gabung) | - |
| **TOTAL KESELURUHAN** | | **2700** | **180** | **180** | **3060** |

---

### 2. Alur Pengolahan Data
Visualisasi berikut menjelaskan bagaimana kategori dataset awal dipetakan ke dalam label yang digunakan oleh model MobileNetV2:

```text
ALUR PENYEDERHANAAN KELAS & DISTRIBUSI DATA
===========================================

[Kategori Dataset]           [Label Akhir]          [Output Model]           [Model .h5]                   [Model.tlite]
                                
Senyum Sedang --------┐                             ┌───────────┐
                      ├───────> SENYUM  ───────────>│   TRAIN   │
Senyum Lebar ---------┘                             │     &     │
                                                    │   VALID   │ Train
Netral -----------------------> NETRAL  ───────────>│     &     │────────>  [ MobileNetV2 ] ───────────> [TensorFLow Lite]
                                                    │    TEST   │
Cemberut Sedang ------┐                             |           |
                      ├───────> CEMBERUT ──────────>|           |
Cemberut Berlebihan --┘                             └───────────┘
                                                          
