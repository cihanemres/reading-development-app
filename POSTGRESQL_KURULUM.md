# PostgreSQL Kurulum Rehberi (Windows)

## Adım 1: PostgreSQL İndirme ve Kurma

1. **PostgreSQL İndir**: https://www.postgresql.org/download/windows/
   - "Download the installer" linkine tıklayın
   - En son sürümü indirin (PostgreSQL 15 veya 16)

2. **Kurulumu Başlat**:
   - İndirilen .exe dosyasını çalıştırın
   - "Next" ile devam edin

3. **Kurulum Ayarları**:
   - Installation Directory: Varsayılan bırakın
   - Components: Tümünü seçili bırakın
   - Data Directory: Varsayılan bırakın
   - **Password**: Bir şifre belirleyin (örn: `postgres`)
     - ⚠️ Bu şifreyi unutmayın!
   - Port: 5432 (varsayılan)
   - Locale: Turkish, Turkey

4. **Kurulumu Tamamla**:
   - "Next" ve "Finish" ile tamamlayın
   - Stack Builder'ı kapatabilirsiniz

## Adım 2: Veritabanı Oluşturma

### Yöntem 1: pgAdmin (Grafiksel Arayüz)

1. **pgAdmin'i Aç**:
   - Başlat menüsünden "pgAdmin 4" arayın
   - Açılan tarayıcı penceresinde bekleyin

2. **Sunucuya Bağlan**:
   - Sol panelde "Servers" > "PostgreSQL 15" (veya 16)
   - Şifrenizi girin (kurulumda belirlediğiniz)

3. **Veritabanı Oluştur**:
   - "Databases" üzerine sağ tıklayın
   - "Create" > "Database..."
   - Database name: `okuma_db`
   - Owner: `postgres`
   - "Save" butonuna tıklayın

### Yöntem 2: SQL Shell (psql)

1. **psql'i Aç**:
   - Başlat menüsünden "SQL Shell (psql)" arayın
   - Enter tuşuna basarak varsayılanları kabul edin
   - Password: Kurulumda belirlediğiniz şifreyi girin

2. **Veritabanı Oluştur**:
   ```sql
   CREATE DATABASE okuma_db;
   ```

3. **Kontrol Et**:
   ```sql
   \l
   ```
   - Listede `okuma_db` görünmeli

## Adım 3: .env Dosyasını Güncelleme

`.env` dosyasını açın ve şifrenizi güncelleyin:

```env
DATABASE_URL=postgresql://postgres:BURAYA_ŞİFRENİZİ_YAZIN@localhost:5432/okuma_db
```

Örnek (şifre `postgres` ise):
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/okuma_db
```

## Adım 4: Kurulumu Test Etme

Proje klasöründe şu komutu çalıştırın:

```bash
python setup.py
```

Başarılı olursa şunu göreceksiniz:
```
✅ Database connection successful!
✅ Tables created successfully!
✅ Admin user created!
```

## Sorun Giderme

### Hata: "could not connect to server"
- PostgreSQL servisinin çalıştığından emin olun:
  - Başlat > "Services" arayın
  - "postgresql-x64-15" (veya 16) servisini bulun
  - Sağ tıklayıp "Start" seçin

### Hata: "password authentication failed"
- `.env` dosyasındaki şifreyi kontrol edin
- PostgreSQL kurulumunda belirlediğiniz şifreyle aynı olmalı

### Hata: "database okuma_db does not exist"
- Adım 2'yi tekrar yapın
- Veritabanını oluşturun

## Hazır!

PostgreSQL kurulumu tamamlandı. Artık uygulamayı çalıştırabilirsiniz:

```bash
# Backend'i başlat
cd backend
python -m uvicorn main:app --reload

# Yeni terminal'de frontend'i başlat
cd frontend
python -m http.server 3000
```

Tarayıcıda: http://localhost:3000
