from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(200), nullable=False)

    profile_image = db.Column(
        db.String(200),
        default=""
    )


class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    title = db.Column(db.String(200), nullable=False)

    description = db.Column(db.Text)

    start_date = db.Column(db.String(50))

    end_date = db.Column(db.String(50))

    budget = db.Column(db.Float, default=0)

    cover_image = db.Column(db.String(200))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    stops = db.relationship(
        "Stop",
        cascade="all, delete",
        backref="trip",
        lazy=True
    )


class Stop(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    trip_id = db.Column(db.Integer, db.ForeignKey("trip.id"))

    city = db.Column(db.String(100))

    country = db.Column(db.String(100))

    start_date = db.Column(db.String(50))

    end_date = db.Column(db.String(50))

    activity = db.relationship(
        "Activity",
        cascade="all, delete",
        backref="stop",
        lazy=True
    )


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    stop_id = db.Column(db.Integer, db.ForeignKey("stop.id"))

    title = db.Column(db.String(200))

    category = db.Column(db.String(100))

    cost = db.Column(db.Float, default=0)

    notes = db.Column(db.Text)


class PackingItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    trip_id = db.Column(db.Integer, db.ForeignKey("trip.id"))

    item_name = db.Column(db.String(200))

    packed = db.Column(db.Boolean, default=False)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    trip_id = db.Column(db.Integer, db.ForeignKey("trip.id"))

    content = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)