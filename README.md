# UnoBot Tracker

🤖 **Bot Telegram untuk melacak poin pemain UnoBot**  

Bot ini otomatis mendeteksi kemenangan pemain di grup Telegram dari pesan bot game seperti:
- `@MauMauMauMauBot`
- `@play_unobot`

Dan memberikan **poin otomatis** kepada pemain yang menang.

---

## ⚡ Fitur Utama
- 🏆 **Leaderboard**: `/leaderboard` menampilkan peringkat pemain.  
- 📝 **Cek poin per user**: `/cekpoin` menampilkan total poin tiap username.  
- ➕ **Tambah poin manual (admin)**: `/addpoin @username [jumlah]`  
- 🔄 **Reset skor (admin)**: `/reset`  
- 📜 **Menu dan edit pesan (admin)**: `/menuuno` dan `/editpesan`  
- ⚡ **Auto detect**: Pesan `@username won!` → bot otomatis menambahkan 1 poin.  
- 🎯 **Game ended!** → bot otomatis balas: `lanjutla tol poin nya kentang kali tu`.  

---

## 🛠 Cara Deploy di Render (Gratis)
1. Hubungkan akun GitHub ke Render.  
2. Buat **New Web Service** → pilih repo ini.  
3. Runtime: **Python**  
4. Build Command: `pip install -r requirements.txt`  
5. Start Command: `python main.py`  
6. Tambahkan Environment Variable:
   - **Key:** `TELEGRAM_BOT_TOKEN`  
   - **Value:** `<masukkan token bot kamu>`  

Render akan otomatis menjalankan bot 24 jam (walau 15 menit idle bot bisa tidur sebentar tapi auto wake).

---

## 🏷 File dalam Repo
- `main.py` → Script utama bot  
- `data.json` → Menyimpan poin pemain  
- `config.json` → Konfigurasi opsional  
- `requirements.txt` → Daftar library Python  
- `README.md` → Dokumentasi ini  

---

## 📌 Tips
- Pastikan token bot Telegram sudah benar.  
- Admin grup Telegram yang bisa akses `/addpoin`, `/reset`, `/menuuno`, `/editpesan`.  
- Gunakan username Telegram dengan `@` saat menambah poin manual.  

---

Bersiaplah melihat bot kamu **jalan otomatis** dan poin pemain tercatat real-time di grup! 🚀
