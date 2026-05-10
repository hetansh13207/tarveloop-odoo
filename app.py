import os
from werkzeug.utils import secure_filename
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    flash,
    session,
    request
)
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from models import (
    db,
    User,
    Trip,
    Stop,
    Activity,
    PackingItem,
    Note
)
from forms import (
    RegisterForm,
    LoginForm,
    TripForm,
    StopForm,
    ActivityForm,
    PackingForm,
    NoteForm,
    ProfileForm
)

DEST_IMG_MAP = {
    'paris':         'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=800&q=80',
    'tokyo':         'https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=800&q=80',
    'dubai':         'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=800&q=80',
    'new york':      'https://images.unsplash.com/photo-1499092346589-b9b6be3e94b2?w=800&q=80',
    'bali':          'https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=800&q=80',
    'santorini':     'https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=800&q=80',
    'kyoto':         'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=800&q=80',
    'maldives':      'https://images.unsplash.com/photo-1514282401047-d79a71a590e8?w=800&q=80',
    'marrakech':     'https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=800&q=80',
    'reykjavik':     'https://images.unsplash.com/photo-1520769945061-0a448c463865?w=800&q=80',
    'goa':           'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=800&q=80',
    'london':        'https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=800&q=80',
    'rome':          'https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=800&q=80',
    'barcelona':     'https://images.unsplash.com/photo-1583422409516-2895a77efded?w=800&q=80',
    'amsterdam':     'https://images.unsplash.com/photo-1534351590666-13e3e96b5702?w=800&q=80',
    'sydney':        'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80',
    'singapore':     'https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=800&q=80',
    'istanbul':      'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=800&q=80',
    'prague':        'https://images.unsplash.com/photo-1541849546-216549ae216d?w=800&q=80',
    'vienna':        'https://images.unsplash.com/photo-1516550893923-42d28e5677af?w=800&q=80',
    'bangkok':       'https://images.unsplash.com/photo-1563492065599-3520f775eeed?w=800&q=80',
    'mumbai':        'https://images.unsplash.com/photo-1570168007204-dfb528c6958f?w=800&q=80',
    'delhi':         'https://images.unsplash.com/photo-1587474260584-136574528ed5?w=800&q=80',
    'los angeles':   'https://images.unsplash.com/photo-1534430480872-3498386e7856?w=800&q=80',
    'san francisco': 'https://images.unsplash.com/photo-1501594907352-04cda38ebc29?w=800&q=80',
    'new zealand':   'https://images.unsplash.com/photo-1507699622108-4be3abd695ad?w=800&q=80',
    'venice':        'https://images.unsplash.com/photo-1534113414509-0eec2bfb493f?w=800&q=80',
    'cairo':         'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=800&q=80',
    'rio':           'https://images.unsplash.com/photo-1483729558449-99ef09a8c325?w=800&q=80',
    'cape town':     'https://images.unsplash.com/photo-1580060839134-75a5edca2e99?w=800&q=80',
    'seoul':         'https://images.unsplash.com/photo-1538485399081-7191377e8241?w=800&q=80',
    'hong kong':     'https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=800&q=80',
    'lisbon':        'https://images.unsplash.com/photo-1555881400-74d7acaacd8b?w=800&q=80',
    'moscow':        'https://images.unsplash.com/photo-1513326738677-b964603b136d?w=800&q=80',
    'berlin':        'https://images.unsplash.com/photo-1560930950-5cc20e80e392?w=800&q=80',
    'zurich':        'https://images.unsplash.com/photo-1515488764276-beab7607c1e6?w=800&q=80',
    'miami':         'https://images.unsplash.com/photo-1506966953602-c20cc11f75e3?w=800&q=80',
    'hawaii':        'https://images.unsplash.com/photo-1542259009477-d625272157b7?w=800&q=80',
    'florence':      'https://images.unsplash.com/photo-1541370976299-4d24be80ec87?w=800&q=80',
    'dubrovnik':     'https://images.unsplash.com/photo-1555990538-c4dc0a5e1bd5?w=800&q=80',
    'phuket':        'https://images.unsplash.com/photo-1589394815804-964ed0be2eb5?w=800&q=80',
}


FALLBACK_TRAVEL_IMGS = [
    'https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=800&q=80',
    'https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=800&q=80',
    'https://images.unsplash.com/photo-1530521954074-e64f6810b32d?w=800&q=80',
    'https://images.unsplash.com/photo-1488085061387-422e29b40080?w=800&q=80',
    'https://images.unsplash.com/photo-1527631746610-bca00a040d60?w=800&q=80',
    'https://images.unsplash.com/photo-1503220317375-aaad61436b1b?w=800&q=80',
    'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80',
    'https://images.unsplash.com/photo-1500835556837-99ac94a94552?w=800&q=80',
    'https://images.unsplash.com/photo-1452421822248-d4c2b47f0c81?w=800&q=80',
    'https://images.unsplash.com/photo-1473186578172-c141e6798cf4?w=800&q=80',
    'https://images.unsplash.com/photo-1519659528534-7fd733a832a0?w=800&q=80',
    'https://images.unsplash.com/photo-1548574505-5e239809ee19?w=800&q=80',
]


def dest_img(city, country=''):
    key = (city or '').strip().lower()
    if key in DEST_IMG_MAP:
        return DEST_IMG_MAP[key]
    seed = sum(ord(c) for c in (city or '') + (country or ''))
    return FALLBACK_TRAVEL_IMGS[seed % len(FALLBACK_TRAVEL_IMGS)]


DEFAULT_ACTIVITY_IMG = 'https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=600&q=80'

# Each entry: (list_of_keywords, image_url)
# Put MULTI-WORD phrases first within each group — they are checked in pass-1
# so "food tour" beats the generic word "tour" which might appear elsewhere.
ACTIVITY_KEYWORD_IMGS = [
    # ── Desert / Dunes ──
    (['desert safari', 'sand dunes', 'camel ride', 'sahara',
      'desert', 'dune', 'camel'],
     'https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=600&q=80'),
    # ── Wildlife Safari ──
    (['game drive', 'national park', 'wildlife safari',
      'safari', 'wildlife', 'lion', 'elephant', 'savanna'],
     'https://images.unsplash.com/photo-1516426122078-c23e76319801?w=600&q=80'),
    # ── Racing / Motorsport ──
    (['car race', 'go kart', 'go-kart', 'motor race', 'formula one',
      'racing', 'karting', 'motorsport', 'circuit'],
     'https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=600&q=80'),
    # ── Beach / Water Sports ──
    (['beach party', 'beach volleyball', 'water sport',
      'beach', 'swim', 'snorkel', 'surfing', 'surf', 'sunbathe', 'coastal'],
     'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&q=80'),
    # ── Scuba / Diving ──
    (['scuba diving', 'underwater cave',
      'scuba', 'dive', 'diving', 'underwater', 'coral'],
     'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=600&q=80'),
    # ── Skiing / Snow ──
    (['snow sport', 'ski resort',
      'ski', 'skiing', 'snowboard', 'snowboarding', 'alpine'],
     'https://images.unsplash.com/photo-1534787238916-9ba6764efd4f?w=600&q=80'),
    # ── Hiking / Trekking ──
    (['mountain trek', 'mountain hike', 'trail run',
      'hike', 'hiking', 'trek', 'trekking', 'trail', 'summit', 'climb', 'mountain'],
     'https://images.unsplash.com/photo-1551632811-561732d1e306?w=600&q=80'),
    # ── Extreme / Adventure ──
    (['bungee jumping', 'sky dive', 'white water',
      'bungee', 'skydive', 'paraglide', 'zipline', 'rafting', 'kayak', 'extreme'],
     'https://images.unsplash.com/photo-1601024445121-e5b82f020549?w=600&q=80'),
    # ── Food / Dining ──  (multi-word phrases FIRST so "food tour" beats "tour" below)
    (['food tour', 'street food', 'cooking class', 'food tasting', 'wine tasting',
      'food', 'eat', 'restaurant', 'dinner', 'lunch', 'breakfast', 'cuisine',
      'culinary', 'chef', 'bbq', 'grill', 'tasting'],
     'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=600&q=80'),
    # ── Wine ──
    (['vineyard tour', 'wine cellar',
      'wine', 'vineyard', 'winery', 'cellar'],
     'https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=600&q=80'),
    # ── Museums / Heritage ──
    (['art gallery', 'history museum', 'natural history',
      'museum', 'gallery', 'exhibition', 'monument', 'heritage', 'ruins', 'palace'],
     'https://images.unsplash.com/photo-1566438480900-0609be27a4be?w=600&q=80'),
    # ── Religious / Temples ──
    (['temple visit', 'church visit',
      'temple', 'church', 'mosque', 'cathedral', 'shrine', 'monastery'],
     'https://images.unsplash.com/photo-1548013146-72479768bada?w=600&q=80'),
    # ── Famous Landmarks ──
    (['eiffel tower', 'great wall', 'taj mahal', 'times square',
      'eiffel', 'colosseum', 'parthenon', 'landmark'],
     'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=600&q=80'),
    # ── City Sightseeing ──  ('tour' only after food-tour already matched above)
    (['city tour', 'walking tour', 'bus tour', 'boat tour',
      'sightseeing', 'guided tour', 'tour'],
     'https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=600&q=80'),
    # ── Shopping / Markets ──
    (['night market', 'flea market',
      'market', 'bazaar', 'souk', 'shopping', 'mall'],
     'https://images.unsplash.com/photo-1555529669-2269763671c0?w=600&q=80'),
    # ── Wellness / Spa ──
    (['hot spring', 'yoga retreat', 'meditation retreat',
      'spa', 'massage', 'wellness', 'yoga', 'meditation', 'relax', 'retreat'],
     'https://images.unsplash.com/photo-1544161515-4ab6ce6db874?w=600&q=80'),
    # ── Nightlife / Entertainment ──
    (['night club', 'live music', 'rooftop bar',
      'concert', 'show', 'theatre', 'theater', 'performance', 'festival',
      'nightlife', 'bar', 'pub', 'club', 'party', 'dance'],
     'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=600&q=80'),
    # ── Cruises / Boats ──
    (['boat ride', 'river cruise',
      'cruise', 'boat', 'sail', 'yacht', 'ferry'],
     'https://images.unsplash.com/photo-1548574505-5e239809ee19?w=600&q=80'),
    # ── Nature / Waterfalls ──
    (['hot spring', 'river rafting',
      'waterfall', 'river', 'lake', 'nature walk'],
     'https://images.unsplash.com/photo-1432405972618-c60b0225b8f9?w=600&q=80'),
    # ── Cycling ──
    (['cycling tour', 'bike ride',
      'cycling', 'bike', 'bicycle'],
     'https://images.unsplash.com/photo-1541625602330-2277a4c46182?w=600&q=80'),
    # ── Zoo / Animals ──
    (['wildlife park', 'animal sanctuary',
      'zoo', 'aquarium', 'animal'],
     'https://images.unsplash.com/photo-1564349683136-77e08dba1ef7?w=600&q=80'),
    # ── Hot Air Balloon ──
    (['hot air balloon',
      'balloon', 'ballooning'],
     'https://images.unsplash.com/photo-1507608616759-54f48f0af0ee?w=600&q=80'),
    # ── Geology / Caves ──
    (['lava field',
      'volcano', 'lava', 'cave', 'canyon'],
     'https://images.unsplash.com/photo-1570093155-da5b0fb8e44e?w=600&q=80'),
    # ── Golf ──
    (['golf course',
      'golf', 'golfing'],
     'https://images.unsplash.com/photo-1535131749006-b7f58c99034b?w=600&q=80'),
    # ── Photography ──
    (['photo walk', 'photography tour',
      'photography', 'camera', 'sunset', 'sunrise'],
     'https://images.unsplash.com/photo-1452421822248-d4c2b47f0c81?w=600&q=80'),
]

ACTIVITY_CATEGORY_IMGS = {
    'sightseeing':   'https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=600&q=80',
    'food':          'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=600&q=80',
    'adventure':     'https://images.unsplash.com/photo-1601024445121-e5b82f020549?w=600&q=80',
    'entertainment': 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=600&q=80',
    'culture':       'https://images.unsplash.com/photo-1566438480900-0609be27a4be?w=600&q=80',
    'nature':        'https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?w=600&q=80',
    'shopping':      'https://images.unsplash.com/photo-1555529669-2269763671c0?w=600&q=80',
    'wellness':      'https://images.unsplash.com/photo-1544161515-4ab6ce6db874?w=600&q=80',
    'sport':         'https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=600&q=80',
    'transport':     'https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=600&q=80',
}


def activity_img(title, category=''):
    text = (title or '').lower() + ' ' + (category or '').lower()

    # Pass 1 — multi-word phrases only (most precise, avoids false matches)
    for keywords, url in ACTIVITY_KEYWORD_IMGS:
        if any(' ' in kw and kw in text for kw in keywords):
            return url

    # Pass 2 — single words
    for keywords, url in ACTIVITY_KEYWORD_IMGS:
        if any(' ' not in kw and kw in text for kw in keywords):
            return url

    # Pass 3 — category fallback
    cat_key = (category or '').strip().lower()
    if cat_key in ACTIVITY_CATEGORY_IMGS:
        return ACTIVITY_CATEGORY_IMGS[cat_key]

    return DEFAULT_ACTIVITY_IMG


cities_data = [
    {
        "name": "Paris",
        "country": "France",
        "cost": "High",
        "image": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34"
    },
    {
        "name": "Tokyo",
        "country": "Japan",
        "cost": "High",
        "image": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf"
    },
    {
        "name": "Dubai",
        "country": "UAE",
        "cost": "Medium",
        "image": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c"
    },
    {
        "name": "Goa",
        "country": "India",
        "cost": "Low",
        "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2"
    },
    {
        "name": "New York",
        "country": "USA",
        "cost": "High",
        "image": "https://images.unsplash.com/photo-1499092346589-b9b6be3e94b2"
    }
]

activities_data = [
    {
        "title": "Eiffel Tower Visit",
        "category": "Sightseeing",
        "cost": 2000
    },
    {
        "title": "Tokyo Food Tour",
        "category": "Food",
        "cost": 3500
    },
    {
        "title": "Desert Safari",
        "category": "Adventure",
        "cost": 5000
    },
    {
        "title": "Beach Party",
        "category": "Entertainment",
        "cost": 1500
    },
    {
        "title": "Museum Tour",
        "category": "Culture",
        "cost": 1000
    }
]

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False

app.config.from_object(Config)

db.init_app(app)

app.jinja_env.globals['dest_img'] = dest_img
app.jinja_env.globals['activity_img'] = activity_img

login_manager = LoginManager()

login_manager.login_view = "login"

login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
@login_required
def home():

    recent_trips = Trip.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Trip.created_at.desc()
    ).limit(3)

    total_trips = Trip.query.filter_by(
        user_id=current_user.id
    ).count()

    all_trips = Trip.query.filter_by(
        user_id=current_user.id
    ).all()

    total_budget = 0

    for trip in all_trips:
        total_budget += trip.budget

    total_stops = Stop.query.join(Trip).filter(
        Trip.user_id == current_user.id
    ).count()

    return render_template(
        "dashboard.html",
        trips=recent_trips,
        total_trips=total_trips,
        total_budget=total_budget,
        total_stops=total_stops
    )

@app.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = RegisterForm()

    if form.validate_on_submit():

        existing_user = User.query.filter_by(
            email=form.email.data
        ).first()

        if existing_user:
            flash("Email already exists")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(form.password.data)

        user = User(
            name=form.name.data,
            email=form.email.data,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration successful")

        return redirect(url_for("login"))

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        if user and check_password_hash(
            user.password,
            form.password.data
        ):

            login_user(user)

            flash("Login successful")

            return redirect(url_for("home"))

        else:
            flash("Invalid email or password")

    return render_template("login.html", form=form)

@app.route("/create-trip", methods=["GET", "POST"])
@login_required
def create_trip():

    form = TripForm()

    if form.validate_on_submit():

        trip = Trip(
            user_id=current_user.id,
            title=form.title.data,
            description=form.description.data,
            start_date=str(form.start_date.data),
            end_date=str(form.end_date.data),
            budget=float(form.budget.data or 0)
        )

        db.session.add(trip)

        db.session.commit()

        flash("Trip created successfully")

        return redirect(url_for("trips"))

    return render_template(
        "create_trip.html",
        form=form
    )

@app.route("/trips")
@login_required
def trips():

    user_trips = Trip.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "trips.html",
        trips=user_trips
    )

@app.route("/trip/<int:trip_id>")
@login_required
def itinerary(trip_id):

    trip = Trip.query.get_or_404(trip_id)

    stops = Stop.query.filter_by(
        trip_id=trip.id
    ).all()

    return render_template(
        "itinerary.html",
        trip=trip,
        stops=stops
    )

@app.route("/trip/<int:trip_id>/add-stop", methods=["GET", "POST"])
@login_required
def add_stop(trip_id):

    trip = Trip.query.get_or_404(trip_id)

    form = StopForm()

    if form.validate_on_submit():

        stop = Stop(
            trip_id=trip.id,
            city=form.city.data,
            country=form.country.data,
            start_date=str(form.start_date.data),
            end_date=str(form.end_date.data)
        )

        db.session.add(stop)

        db.session.commit()

        flash("Stop added successfully")

        return redirect(
            url_for(
                "itinerary",
                trip_id=trip.id
            )
        )

    return render_template(
        "add_stop.html",
        form=form,
        trip=trip
    )

@app.route("/stop/<int:stop_id>/add-activity", methods=["GET", "POST"])
@login_required
def add_activity(stop_id):

    stop = Stop.query.get_or_404(stop_id)

    form = ActivityForm()

    if form.validate_on_submit():

        activity = Activity(
            stop_id=stop.id,
            title=form.title.data,
            category=form.category.data,
            cost=float(form.cost.data or 0),
            notes=form.notes.data
        )

        db.session.add(activity)

        db.session.commit()

        flash("Activity added")

        return redirect(
            url_for(
                "itinerary",
                trip_id=stop.trip_id
            )
        )

    return render_template(
        "activity_search.html",
        form=form,
        stop=stop
    )

@app.route("/trip/<int:trip_id>/budget")
@login_required
def budget(trip_id):

    trip = Trip.query.get_or_404(trip_id)

    stops = Stop.query.filter_by(
        trip_id=trip.id
    ).all()

    total_activity_cost = 0

    total_activities = 0

    for stop in stops:

        activities = Activity.query.filter_by(
            stop_id=stop.id
        ).all()

        for activity in activities:

            total_activity_cost += activity.cost

            total_activities += 1

    remaining_budget = trip.budget - total_activity_cost

    return render_template(
        "budget.html",
        trip=trip,
        total_activity_cost=total_activity_cost,
        remaining_budget=remaining_budget,
        total_activities=total_activities
    )

@app.route("/trip/<int:trip_id>/packing", methods=["GET", "POST"])
@login_required
def packing(trip_id):

    trip = Trip.query.get_or_404(trip_id)

    form = PackingForm()

    if form.validate_on_submit():

        item = PackingItem(
            trip_id=trip.id,
            item_name=form.item_name.data
        )

        db.session.add(item)

        db.session.commit()

        flash("Item added")

        return redirect(
            url_for(
                "packing",
                trip_id=trip.id
            )
        )

    items = PackingItem.query.filter_by(
        trip_id=trip.id
    ).all()

    return render_template(
        "packing.html",
        trip=trip,
        items=items,
        form=form
    )

@app.route("/packing/<int:item_id>/toggle")
@login_required
def toggle_packing(item_id):

    item = PackingItem.query.get_or_404(item_id)

    item.packed = not item.packed

    db.session.commit()

    return redirect(
        url_for(
            "packing",
            trip_id=item.trip_id
        )
    )

@app.route("/trip/<int:trip_id>/notes", methods=["GET", "POST"])
@login_required
def notes(trip_id):

    trip = Trip.query.get_or_404(trip_id)

    form = NoteForm()

    if form.validate_on_submit():

        note = Note(
            trip_id=trip.id,
            content=form.content.data
        )

        db.session.add(note)

        db.session.commit()

        flash("Note added")

        return redirect(
            url_for(
                "notes",
                trip_id=trip.id
            )
        )

    trip_notes = Note.query.filter_by(
        trip_id=trip.id
    ).order_by(Note.created_at.desc()).all()

    return render_template(
        "notes.html",
        trip=trip,
        notes=trip_notes,
        form=form
    )

@app.route("/trip/<int:trip_id>/delete")
@login_required
def delete_trip(trip_id):

    trip = Trip.query.get_or_404(trip_id)

    if trip.user_id != current_user.id:
        flash("Unauthorized")
        return redirect(url_for("trips"))

    db.session.delete(trip)

    db.session.commit()

    flash("Trip deleted")

    return redirect(url_for("trips"))

@app.route("/stop/<int:stop_id>/delete")
@login_required
def delete_stop(stop_id):

    stop = Stop.query.get_or_404(stop_id)

    trip_id = stop.trip_id

    db.session.delete(stop)

    db.session.commit()

    flash("Stop deleted")

    return redirect(
        url_for(
            "itinerary",
            trip_id=trip_id
        )
    )

@app.route("/activity/<int:activity_id>/delete")
@login_required
def delete_activity(activity_id):

    activity = Activity.query.get_or_404(activity_id)

    trip_id = activity.stop.trip_id

    db.session.delete(activity)

    db.session.commit()

    flash("Activity deleted")

    return redirect(
        url_for(
            "itinerary",
            trip_id=trip_id
        )
    )

@app.route("/note/<int:note_id>/delete")
@login_required
def delete_note(note_id):

    note = Note.query.get_or_404(note_id)

    trip_id = note.trip_id

    db.session.delete(note)

    db.session.commit()

    flash("Note deleted")

    return redirect(
        url_for(
            "notes",
            trip_id=trip_id
        )
    )

@app.route("/public/trip/<int:trip_id>")
def public_trip(trip_id):

    trip = Trip.query.get_or_404(trip_id)

    stops = Stop.query.filter_by(
        trip_id=trip.id
    ).all()

    return render_template(
        "public_trip.html",
        trip=trip,
        stops=stops
    )

@app.route("/city-search")
@login_required
def city_search():

    query = request.args.get("query", "").lower()

    filtered_cities = cities_data

    if query:

        filtered_cities = []

        for city in cities_data:

            if (
                query in city["name"].lower()
                or
                query in city["country"].lower()
            ):

                filtered_cities.append(city)

    return render_template(
        "city_search.html",
        cities=filtered_cities
    )

@app.route("/activity-discovery")
@login_required
def activity_discovery():

    query = request.args.get("query", "").lower()

    filtered_activities = activities_data

    if query:

        filtered_activities = []

        for activity in activities_data:

            if (
                query in activity["title"].lower()
                or
                query in activity["category"].lower()
            ):

                filtered_activities.append(activity)

    return render_template(
        "activity_search.html",
        activities=filtered_activities
    )

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    form = ProfileForm()

    if request.method == "GET":

        form.name.data = current_user.name

    if form.validate_on_submit():

        current_user.name = form.name.data

        if form.profile_image.data:

            image = form.profile_image.data

            filename = secure_filename(image.filename)

            image_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )

            image.save(image_path)

            current_user.profile_image = filename

        db.session.commit()

        flash("Profile updated")

        return redirect(url_for("profile"))

    return render_template(
        "profile.html",
        form=form
    )

@app.route("/admin")
@login_required
def admin_dashboard():

    total_users = User.query.count()

    total_trips = Trip.query.count()

    total_stops = Stop.query.count()

    total_activities = Activity.query.count()

    all_stops = Stop.query.all()

    city_count = {}

    for stop in all_stops:

        city = stop.city

        if city in city_count:

            city_count[city] += 1

        else:

            city_count[city] = 1

    popular_cities = sorted(
        city_count.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_trips=total_trips,
        total_stops=total_stops,
        total_activities=total_activities,
        popular_cities=popular_cities
    )

@app.route("/logout")
@login_required
def logout():

    logout_user()

    session.clear()

    flash("Logged out successfully")

    return redirect(url_for("login"))

@app.after_request
def add_header(response):

    response.cache_control.no_store = True
    response.cache_control.no_cache = True
    response.cache_control.must_revalidate = True
    response.cache_control.max_age = 0

    return response

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    host = "0.0.0.0" if os.environ.get("REPLIT_DEV_DOMAIN") else "127.0.0.1"
    app.run(debug=True, host=host, port=port)