# Okuma Geliştirme Uygulaması - Hızlı Başlangıç

## Kurulum Adımları

### 1. PostgreSQL Kurulumu

PostgreSQL'i indirin ve kurun: https://www.postgresql.org/download/windows/

pgAdmin veya psql ile veritabanı oluşturun:

```sql
CREATE DATABASE okuma_db;
```

### 2. Python Ortamını Hazırlayın

```powershell
# Sanal ortam oluştur
python -m venv venv

# Sanal ortamı aktif et
.\venv\Scripts\activate

# Bağımlılıkları yükle
pip install -r backend\requirements.txt
```

### 3. Ortam Değişkenlerini Ayarlayın

`.env.example` dosyasını `.env` olarak kopyalayın:

```powershell
copy .env.example .env
```

`.env` dosyasını düzenleyin ve PostgreSQL bilgilerinizi girin:

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/okuma_db
SECRET_KEY=gizli-anahtar-buraya-yazin
```

### 4. Backend'i Başlatın

```powershell
cd backend
python -m uvicorn main:app --reload
```

Backend şu adreste çalışacak: http://localhost:8000

API Dokümantasyonu: http://localhost:8000/docs

### 5. Frontend'i Başlatın

Yeni bir terminal açın:

```powershell
cd frontend
python -m http.server 3000
```

Frontend şu adreste çalışacak: http://localhost:3000

### 6. İlk Admin Kullanıcısını Oluşturun

Python shell'i açın:

```powershell
python
```

Şu kodu çalıştırın:

```python
from backend.models.user import User, UserRole
from backend.auth.password import hash_password
from backend.database import SessionLocal

db = SessionLocal()

admin = User(
    ad_soyad="Yönetici",
    email="admin@okuma.com",
    password_hash=hash_password("admin123"),
    rol=UserRole.ADMIN
)

db.add(admin)
db.commit()
print("Admin kullanıcı oluşturuldu!")
```

### 7. Giriş Yapın

http://localhost:3000/login.html adresine gidin

- Email: admin@okuma.com
- Şifre: admin123

## Sorun Giderme

### PostgreSQL Bağlantı Hatası

- PostgreSQL servisinin çalıştığından emin olun
- `.env` dosyasındaki DATABASE_URL'i kontrol edin
- Şifre ve kullanıcı adını doğrulayın

### Port Zaten Kullanımda

Backend için farklı port:
```powershell
python -m uvicorn main:app --reload --port 8001
```

Frontend için farklı port:
```powershell
python -m http.server 3001
```

### Modül Bulunamadı Hatası

Sanal ortamın aktif olduğundan emin olun:
```powershell
.\venv\Scripts\activate
```

Bağımlılıkları tekrar yükleyin:
```powershell
pip install -r backend\requirements.txt
```

## Sonraki Adımlar

1. Admin panelinden hikâye ekleyin
2. Öğrenci, öğretmen ve veli kullanıcıları oluşturun
3. Öğrenci olarak giriş yapıp hikâyeleri test edin

## Yardım

Sorun yaşarsanız README.md dosyasına bakın veya issue açın.
