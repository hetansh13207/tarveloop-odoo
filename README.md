# Traveloop

Traveloop is a full-stack travel planning web application built with Python and Flask. It gives travelers a single place to plan trips, organize daily itineraries, track budgets, and discover activities — all wrapped in a modern glassmorphism dark-themed interface.

---

## Features

### User Authentication
- Secure registration and login system powered by **Flask-Login**.
- Passwords are hashed using **Werkzeug's** `generate_password_hash` / `check_password_hash` before being stored.
- Each user has an isolated view — trips, budgets, and itineraries are all account-specific.
- Profile page lets users update their display name and upload a custom profile photo.

### Trip Management
- Create new trips with a title, destination, start date, and end date.
- View all your trips on a dashboard with quick-access cards.
- Edit or delete trips at any time.
- Each trip acts as a container for itinerary stops, activities, and a budget.

### Itinerary Builder
- Add multiple stops to any trip, each with a city name and country.
- Every stop automatically displays a high-quality destination banner image sourced from a curated map of 40+ cities (Paris, Tokyo, New York, Dubai, etc.).
- For cities not in the curated map, a deterministic fallback picks from a pool of 12 scenic travel images — no broken images ever.

### Activity Search & Saving
- Browse a searchable list of travel activities (tours, adventures, food experiences, etc.).
- Activities are filtered by destination or category.
- Each activity card shows a contextually matched image using a two-pass keyword system:
  - **Pass 1:** Matches multi-word phrases first (e.g. "Desert Safari", "Tokyo Food Tour").
  - **Pass 2:** Falls back to single keyword matching (e.g. "hiking", "museum").
- Save activities to any of your trips for later reference.

### Budget Tracker
- Set a total budget for each trip and log individual expenses with a title, amount, and category.
- Dashboard shows total budget, total spent, and remaining balance at a glance.
- **Live Currency Converter** widget on the budget page:
  - Fetches real-time exchange rates from the free `open.er-api.com` API (no API key required).
  - Supports 12 major currencies: USD, EUR, GBP, INR, AED, JPY, CAD, AUD, CHF, SGD, MYR, THB.
  - Instantly converts your Budget, Spent, and Remaining values on currency selection.

### UI & Design
- **Glassmorphism** design system — frosted-glass cards with backdrop blur, soft borders, and layered depth.
- **Dark theme** throughout with a cohesive dark navy/indigo color palette.
- Animated **infinity loop SVG logo** in the navbar, reinforcing the "loop" in Traveloop.
- Smooth **fade-up entrance animations** on cards and page sections using CSS keyframes.
- Flash messages for success/error feedback styled to match the glassmorphism theme.
- Fully responsive layout built with CSS Flexbox and Grid.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| Web Framework | Flask |
| Authentication | Flask-Login |
| Forms & CSRF | Flask-WTF |
| Database ORM | SQLAlchemy (via Flask-SQLAlchemy) |
| Database | SQLite |
| Password Security | Werkzeug |
| Templating | Jinja2 |
| Frontend | Vanilla CSS, Vanilla JavaScript |
| Exchange Rates API | open.er-api.com (free, no key) |
| Image Sources | Unsplash (curated static URLs) |

---

## Project Structure

```
traveloop/
├── app.py              # Main Flask app, routes, image logic
├── config.py           # App configuration and session settings
├── models.py           # SQLAlchemy database models
├── forms.py            # Flask-WTF form definitions
├── templates/
│   ├── base.html       # Navbar, footer, flash messages
│   ├── index.html      # Landing / dashboard
│   ├── trip.html       # Trip detail view
│   ├── itinerary.html  # Itinerary stops
│   ├── activity_search.html  # Activity browser
│   ├── budget.html     # Budget tracker + currency converter
│   └── profile.html    # User profile settings
├── static/
│   ├── css/style.css   # Full glassmorphism stylesheet
│   └── js/main.js      # Theme, animations, file input handler
└── instance/
    └── database.db     # SQLite database (auto-created)
```

---

## Getting Started

1. Install dependencies:
   ```bash
   pip install flask flask-login flask-wtf flask-sqlalchemy werkzeug
   ```
2. Run the app:
   ```bash
   python app.py
   ```
3. Open `http://localhost:5000` in your browser and register an account.

---

## Credits

Cooked by [Hetansh Darji](https://www.linkedin.com/in/hetansh-darji-603b72263/) · [Deep Prajapati](https://www.linkedin.com/in/deep-prajapati-46b820331/) · [Krish Mahyavanshi](https://www.linkedin.com/in/krish-mahyavanshi-1651421b5/)
