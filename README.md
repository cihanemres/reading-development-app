# Okuma Geliştirme Web Uygulaması

Öğrencilerin okuma becerilerini geliştirmek için tasarlanmış kapsamlı bir web platformu. Öğrenci, öğretmen, veli ve yönetici rolleri ile tam özellikli bir eğitim sistemi.

## 🚀 Özellikler

### Öğrenci Modülü
- ⏱️ Zamanlı okuma (kronometre ile)
- 🎧 Sesli hikâye dinleme
- 📝 Tekrarlı pratik yapma
- ❓ Anlama testleri (çoktan seçmeli + açık uçlu)
- 📊 İlerleme grafikleri ve raporlar

### Öğretmen Paneli
- 👥 Öğrenci listesi ve takibi
- 📈 Detaylı ilerleme raporları
- ✍️ Değerlendirme ve puanlama
- 💬 Geri bildirim ve yorumlar

### Veli Paneli
- 👶 Çocuk gelişimi takibi
- 📋 Öğretmen yorumları
- 💡 Pratik önerileri

### Yönetici Paneli
- 📚 Hikâye yönetimi (CRUD)
- 👤 Kullanıcı yönetimi
- 📤 Dosya yükleme (MP3, resim)
- 📊 Sistem istatistikleri

## 🛠️ Teknoloji Stack

### Backend
- **Framework**: FastAPI 0.104.1
- **Veritabanı**: PostgreSQL
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)

### Frontend
- **HTML5** + **Tailwind CSS**
- **Vanilla JavaScript**
- **Chart.js** (grafikler için)
- **Font Awesome** (ikonlar)

## 📋 Gereksinimler

- Python 3.9+
- PostgreSQL 12+
- Node.js (opsiyonel, frontend geliştirme için)

## 🔧 Kurulum

### 1. Depoyu Klonlayın

```bash
git clone <repository-url>
cd proj
```

### 2. Python Sanal Ortamı Oluşturun

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Bağımlılıkları Yükleyin

```bash
pip install -r backend/requirements.txt
```

### 4. PostgreSQL Veritabanı Oluşturun

```sql
CREATE DATABASE okuma_db;
CREATE USER okuma_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE okuma_db TO okuma_user;
```

### 5. Ortam Değişkenlerini Ayarlayın

`.env.example` dosyasını `.env` olarak kopyalayın ve düzenleyin:

```bash
cp .env.example .env
```

`.env` dosyasını düzenleyin:

```env
DATABASE_URL=postgresql://okuma_user:your_password@localhost:5432/okuma_db
SECRET_KEY=your-very-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

### 6. Veritabanı Tablolarını Oluşturun

Backend uygulaması ilk çalıştırıldığında otomatik olarak tabloları oluşturacaktır.

### 7. Backend Sunucusunu Başlatın

```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API dokümantasyonu: http://localhost:8000/docs

### 8. Frontend'i Çalıştırın

Basit bir HTTP sunucusu ile:

```bash
# Python ile
cd frontend
python -m http.server 3000

# Veya Node.js ile
npx serve frontend -p 3000
```

Uygulama: http://localhost:3000

## 📁 Proje Yapısı

```
proj/
├── backend/
│   ├── main.py                 # FastAPI uygulaması
│   ├── database.py             # Veritabanı bağlantısı
│   ├── requirements.txt        # Python bağımlılıkları
│   ├── models/                 # SQLAlchemy modelleri
│   │   ├── user.py
│   │   ├── story.py
│   │   ├── reading_activity.py
│   │   └── evaluation.py
│   ├── routers/                # API endpoint'leri
│   │   ├── auth.py
│   │   ├── stories.py
│   │   ├── reading.py
│   │   ├── teacher.py
│   │   ├── parent.py
│   │   └── admin.py
│   ├── auth/                   # Authentication
│   │   ├── jwt_handler.py
│   │   ├── password.py
│   │   └── dependencies.py
│   └── utils/                  # Yardımcı fonksiyonlar
│       ├── word_counter.py
│       ├── progress_calculator.py
│       └── file_handler.py
├── frontend/
│   ├── index.html              # Ana sayfa
│   ├── login.html              # Giriş sayfası
│   ├── register.html           # Kayıt sayfası
│   ├── student/                # Öğrenci sayfaları
│   │   └── dashboard.html
│   ├── teacher/                # Öğretmen sayfaları
│   ├── parent/                 # Veli sayfaları
│   ├── admin/                  # Yönetici sayfaları
│   └── js/                     # JavaScript dosyaları
│       ├── api.js
│       └── auth.js
├── static/                     # Statik dosyalar
│   └── uploads/                # Yüklenen dosyalar
│       ├── images/
│       └── audio/
├── .env.example                # Örnek ortam değişkenleri
├── .gitignore
└── README.md
```

## 🔐 Varsayılan Kullanıcılar

İlk yönetici kullanıcısını manuel olarak oluşturmanız gerekir:

```python
# Python shell'de
from backend.models.user import User, UserRole
from backend.auth.password import hash_password
from backend.database import SessionLocal

db = SessionLocal()

admin = User(
    ad_soyad="Admin User",
    email="admin@example.com",
    password_hash=hash_password("admin123"),
    rol=UserRole.ADMIN
)

db.add(admin)
db.commit()
```

## 📚 API Dokümantasyonu

FastAPI otomatik olarak API dokümantasyonu oluşturur:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🎯 Kullanım Akışı

### Öğrenci Akışı
1. Kayıt ol / Giriş yap
2. Sınıf seviyesine uygun hikâyeleri gör
3. Hikâye seç
4. Ön okuma yap (zamanlı)
5. Sesli versiyonu dinle
6. Pratik yap (tekrar oku)
7. Anlama testini çöz
8. İlerlemeyi görüntüle

### Öğretmen Akışı
1. Giriş yap
2. Öğrenci listesini gör
3. Öğrenci ilerlemesini takip et
4. Açık uçlu cevapları değerlendir
5. Geri bildirim ver

### Veli Akışı
1. Giriş yap
2. Çocuğun ilerlemesini gör
3. Öğretmen yorumlarını oku
4. Pratik önerilerini incele

## 🚢 Deployment

### Railway.app (Önerilen)

1. Railway hesabı oluşturun
2. PostgreSQL eklentisi ekleyin
3. GitHub repo'nuzu bağlayın
4. Ortam değişkenlerini ayarlayın
5. Deploy edin

### Render.com

1. Render hesabı oluşturun
2. PostgreSQL veritabanı oluşturun
3. Web servisi oluşturun
4. Ortam değişkenlerini ayarlayın
5. Deploy edin

### Docker (Opsiyonel)

```bash
docker-compose up -d
```

## 🧪 Test

```bash
# Backend testleri
cd backend
pytest

# Frontend testleri (manuel)
# Tarayıcıda sayfaları açın ve test edin
```

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 📧 İletişim

Sorularınız için: [cihanemres@gmail.com](mailto:cihanemresgmail.com)

## 🙏 Teşekkürler

- FastAPI ekibine
- Tailwind CSS ekibine
- Chart.js ekibine
- Font Awesome ekibine

---

**Not**: Bu uygulama eğitim amaçlıdır. Üretim ortamında kullanmadan önce güvenlik önlemlerini gözden geçirin.
