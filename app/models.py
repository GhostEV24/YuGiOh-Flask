from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    collection = db.relationship('Collection', backref='user', lazy=True)
    wishlist = db.relationship('Wishlist', backref='user', lazy=True)

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

# Table pour la wishlist
class Wishlist(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), primary_key=True)

# Table pour la collection
class Collection(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), primary_key=True)
    card = db.relationship("Card", backref="collections")  # Ajoute cette relation

