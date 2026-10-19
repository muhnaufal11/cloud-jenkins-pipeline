# Cloud Jenkins Pipeline

Proyek integrasi Continuous Integration and Continuous Deployment (CI/CD) menggunakan Jenkins, Docker, dan SQLite Database untuk Praktikum Komputasi Awan 2026/2027.

## Arsitektur Proyek
- **Aplikasi**: Python Flask Web Application (`app.py`)
- **Database**: SQLite Database (`database.py`) dengan tabel `server_logs`
- **Kontainerisasi**: Dockerfile berbasis `python:3.10-slim`
- **Otomasi CI/CD**: Jenkinsfile Pipeline terhubung ke GitHub Webhook & Ngrok

## Tahapan Pipeline (Stages)
1. **Checkout SCM**: Mengambil kode sumber terbaru dari repositori GitHub.
2. **Test & DB Initialization**: Verifikasi koneksi dan migrasi skema basis data SQLite.
3. **Build Docker Image**: Membangun image Docker dengan tag build number dan `latest`.
4. **Verify Docker Image**: Memvalidasi image lokal dan ukuran container.
5. **Push Docker Image**: Autentikasi dan pengiriman container image ke registry Docker Hub.
