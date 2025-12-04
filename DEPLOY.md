# 🚀 Deployment Guide - Okuma Geliştirme Uygulaması

## Hızlı Başlangıç (Docker ile)

### 1. Gereksinimler
- Docker ve Docker Compose yüklü olmalı
- Git yüklü olmalı

### 2. Projeyi Klonla
```bash
git clone <repo-url>
cd proj
```

### 3. Environment Dosyasını Hazırla
```bash
cp .env.example .env
# .env dosyasını düzenleyip SECRET_KEY'i değiştirin
```

### 4. Docker ile Çalıştır
```bash
# Tüm servisleri başlat
docker-compose up -d

# Logları izle
docker-compose logs -f
```

### 5. Erişim
- **Frontend:** http://localhost
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## Servisler

| Servis | Port | Açıklama |
|--------|------|----------|
| Frontend (Nginx) | 80 | Static dosyaları sunar, API'yi proxy'ler |
| Backend (FastAPI) | 8000 | REST API |
| PostgreSQL | 5432 | Veritabanı |

---

## Komutlar

```bash
# Başlat
docker-compose up -d

# Durdur
docker-compose down

# Yeniden başlat
docker-compose restart

# Logları gör
docker-compose logs -f backend

# Veritabanını sıfırla (DİKKAT!)
docker-compose down -v
docker-compose up -d
```

---

## Production Checklist ✅

- [ ] SECRET_KEY'i güvenli bir değerle değiştir
- [ ] DEBUG=False olduğundan emin ol
- [ ] HTTPS yapılandır (nginx veya reverse proxy ile)
- [ ] ALLOWED_ORIGINS'i güncelle
- [ ] Veritabanı backup'larını ayarla
- [ ] Log rotation yapılandır
- [ ] Firewall kurallarını ayarla

---

## Cloud Deployment Seçenekleri

### Railway
1. Railway.app'e git ve yeni proje oluştur
2. GitHub reposunu bağla
3. Environment variables'ları ekle
4. Deploy et

### Render
1. render.com'da yeni Web Service oluştur
2. Docker build seç
3. Environment variables'ları ekle
4. Deploy et

### DigitalOcean App Platform
1. DigitalOcean'da App oluştur
2. GitHub reposunu bağla
3. Docker Compose'u yapılandır
4. Deploy et

---

## Sorun Giderme

### Port Çakışması
```bash
# Port 80 kullanımda mı kontrol et
netstat -ano | findstr :80

# docker-compose.yml'da portu değiştir
ports:
  - "8080:80"
```

### Veritabanı Bağlanamıyor
```bash
# PostgreSQL container'ını kontrol et
docker-compose ps
docker-compose logs postgres
```

### Backend Başlamıyor
```bash
# Logları kontrol et
docker-compose logs backend
```
