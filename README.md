# 📈 PaperTrader

A full-stack paper trading simulator built with **Django**, **SQLite**, and the **Finnhub API**. Trade real stocks with $100,000 in virtual money — zero risk, full experience.

**Live Demo:** *(your Render URL here)*

---

## Features

- **Multi-user auth** — register, login, per-user portfolios
- **Live stock prices** — real-time quotes via Finnhub API
- **Buy & Sell** — full order execution with avg cost basis tracking
- **Portfolio growth chart** — visual history of portfolio value over time
- **Full transaction history** — every trade logged with realized P&L, filterable by symbol/action
- **Holdings dashboard** — unrealized P&L per position with live prices
- **Deploy-ready** — configured for Render with `render.yaml`

---

## Tech Stack

| Layer      | Technology              |
|------------|-------------------------|
| Backend    | Python 3.11 + Django 5  |
| Database   | SQLite (dev) / upgradeable to PostgreSQL |
| Frontend   | Django templates + Chart.js |
| Prices     | Finnhub REST API        |
| Deployment | Render (free tier)      |
| Static     | WhiteNoise              |

---

## Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/papertrader.git
cd papertrader
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
```
Edit `.env` and fill in:
```
SECRET_KEY=any-random-secret-string
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
FINNHUB_API_KEY=your_key_from_finnhub.io
```
> Get a **free** Finnhub API key at [finnhub.io/register](https://finnhub.io/register)  
> The app works without a key using mock prices.

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. (Optional) Create a superuser for Django admin
```bash
python manage.py createsuperuser
```

### 7. Start the dev server
```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000** — register an account and start trading!

---

## Deploying to Render (Free)

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit — PaperTrader"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/papertrader.git
git push -u origin main
```

### 2. Create a Render Web Service
1. Go to [render.com](https://render.com) → **New → Web Service**
2. Connect your GitHub repo
3. Render auto-detects `render.yaml` — click **Apply**

### 3. Set environment variables in Render dashboard
| Key | Value |
|-----|-------|
| `SECRET_KEY` | Any long random string |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `your-app-name.onrender.com` |
| `FINNHUB_API_KEY` | Your Finnhub key |

### 4. Deploy
Render runs migrations and collectstatic automatically on deploy.  
Your app will be live at `https://your-app-name.onrender.com`

---

## Project Structure

```
papertrader/
├── papertrader/          # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── trading/              # Main app
│   ├── models.py         # Portfolio, Holding, Transaction, PortfolioSnapshot
│   ├── views.py          # Auth, dashboard, trade, history, API endpoints
│   ├── finnhub.py        # Finnhub API service layer
│   ├── urls.py
│   ├── admin.py
│   └── templates/trading/
│       ├── login.html
│       ├── dashboard.html
│       └── history.html
├── templates/
│   └── base.html         # Shared layout
├── requirements.txt
├── render.yaml           # Render deployment config
├── manage.py
└── .env.example
```

---

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/quote/?symbol=AAPL` | Live price for a symbol |
| `GET /api/chart/` | Portfolio snapshot data for chart |

---

## Models

- **Portfolio** — one per user, tracks cash balance
- **Holding** — current open positions with avg cost basis
- **Transaction** — immutable log of every buy/sell with realized P&L
- **PortfolioSnapshot** — timestamped portfolio value (powers the growth chart)

---

## Screenshots

*(Add screenshots here after deployment)*

---

## License

MIT
