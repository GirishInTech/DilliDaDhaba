# Dilli Da Dhaba 🍛

A **production-ready Django restaurant website** for *Dilli Da Dhaba* — an authentic North Indian restaurant.

---

## 🏗 Project Structure

```
DilliDaDhaba_django/
├── dilli_da_dhaba/          # Django project (settings, root URLs)
├── core/                    # Homepage, About, Contact views
├── menu/                    # Menu models, DRF APIs, admin
├── reviews/                 # Customer testimonials
├── accounts/                # JWT auth endpoints
├── templates/               # Django HTML templates
│   ├── base.html
│   ├── partials/
│   │   ├── navbar.html
│   │   └── footer.html
│   ├── core/
│   │   ├── home.html
│   │   ├── about.html
│   │   └── contact.html
│   └── menu/
│       └── menu.html
├── static/
│   ├── css/styles.css
│   └── js/main.js
├── manage.py
├── requirements.txt
└── .env.example
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5, Django REST Framework |
| Auth | SimpleJWT |
| Frontend | Django Templates + HTMX + Alpine.js |
| Styling | TailwindCSS (CDN) |
| DB (dev) | SQLite |
| DB (prod) | PostgreSQL |
| Images | Pillow + Cloudinary-ready |
| Static | WhiteNoise |

---

## 🚀 Quick Start

### 1. Clone & create virtual environment

```bash
git clone <repo-url>
cd DilliDaDhaba_django

python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
# Edit .env — at minimum set a SECRET_KEY
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000** in your browser.

---

## 🔌 API Endpoints

All APIs are public (read-only).

| Method | URL | Description |
|---|---|---|
| GET | `/api/categories` | All menu categories |
| GET | `/api/menu` | Full available menu |
| GET | `/api/menu?category=<id>` | Items by category |
| GET | `/api/menu?veg=true` | Veg-only items |
| GET | `/api/featured` | Featured / homepage dishes |
| POST | `/api/auth/token/` | Obtain JWT tokens |
| POST | `/api/auth/token/refresh/` | Refresh access token |

---

## 🛠 Admin Panel

Access at **http://127.0.0.1:8000/admin/**

Admin capabilities:
- Add / edit / delete menu items with image upload
- Toggle `featured`, `is_available`, `needs_verification` inline
- Reorder categories via `display_order`
- Approve customer reviews
- Full image preview inside admin list view

---

## 🖼 Cloudinary Image Storage

To switch from local file storage to Cloudinary:

1. Add credentials to `.env`  
2. Uncomment the `CLOUDINARY_STORAGE` block in `settings.py`  
3. `pip install cloudinary django-cloudinary-storage`

---

## 🗃 Database Models

### `Category`
- `name`, `display_order`, `created_at`

### `MenuItem`
- `category` (FK), `name`, `description`, `veg`
- `price_regular`, `price_half`, `price_full`
- `image`, `featured`, `is_available`, `needs_verification`

### `Review`
- `reviewer_name`, `rating` (1–5), `body`, `source`, `is_approved`

---

## 📦 Production Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Set a strong `SECRET_KEY`
- [ ] Configure `DATABASE_URL` → PostgreSQL
- [ ] Configure Cloudinary for image storage
- [ ] Run `python manage.py collectstatic`
- [ ] Serve with Gunicorn behind Nginx
- [ ] Set `ALLOWED_HOSTS` to production domain
- [ ] Enable HTTPS + set `SECURE_SSL_REDIRECT=True`
