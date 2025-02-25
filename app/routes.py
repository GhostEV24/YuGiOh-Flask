from flask import render_template, redirect, url_for, flash, session, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User, Card, Wishlist, Collection
from flask import Blueprint
from app.forms import LoginForm, RegisterForm
import requests

main = Blueprint("main", __name__)


@main.route("/")
def home():
    if not session.get("user_id"):  # Vérifier si l'utilisateur est connecté
        return redirect(url_for('main.index'))  # Rediriger vers la page de connexion et d'inscription
    return render_template("home.html")  # Afficher la page d'accueil si l'utilisateur est connecté



@main.route("/index")
def index():
    return render_template('index.html')  # Page avec juste les options de connexion et inscription

@main.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Compte créé avec succès !", "success")
        return redirect(url_for("main.login"))
    return render_template("register.html", form=form)

@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            session["user_id"] = user.id  # 🔹 Stocke l'ID utilisateur en session
            flash("Connexion réussie !", "success")
            return redirect(url_for("main.home"))
        else:
            flash("Identifiants incorrects.", "danger")
    return render_template("login.html", form=form)

@main.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop("user_id", None)  # 🔹 Supprime l'ID utilisateur de la session
    flash("Déconnexion réussie.", "info")
    return redirect(url_for("main.login"))

API_URL = "https://db.ygoprodeck.com/api/v7/cardinfo.php?language=fr&fname=Temps"

@main.route('/cards')
def get_cards():
    response = requests.get(API_URL)
    
    if response.status_code == 200:
        cards_data = response.json()
        cards_with_sets = []

        for card in cards_data['data']:
            card_info = {
                "id": card["id"],
                "name": card["name"],
                "type": card["type"],
                "description": card["desc"],
                "card_sets": card.get("card_sets", []),
                "image_url": card["card_images"][0]["image_url"] if card["card_images"] else None,
            }
            cards_with_sets.append(card_info)

        return render_template('cards.html', cards=cards_with_sets, user_id=session.get("user_id"))
    else:
        flash("Erreur lors de la récupération des cartes", "danger")
        return redirect(url_for('main.home'))

@main.route('/wishlist/add/<int:card_id>', methods=['POST'])
@login_required
def add_to_wishlist(card_id):
    user = User.query.get(session["user_id"])
    card = Card.query.get(card_id)

    if not user or not card:
        return jsonify({"error": "Utilisateur ou carte non trouvée"}), 404

    if not Wishlist.query.filter_by(user_id=user.id, card_id=card.id).first():
        wishlist_entry = Wishlist(user_id=user.id, card_id=card.id)
        db.session.add(wishlist_entry)
        db.session.commit()
        return jsonify({"message": f"La carte {card.name} a été ajoutée à la wishlist de {user.username}."}), 200
    else:
        return jsonify({"message": "La carte est déjà dans la wishlist."}), 200

@main.route('/collection/add/<int:user_id>/<int:card_id>', methods=['POST'])
@login_required
def add_to_collection(user_id, card_id):
    # Vérifier si l'utilisateur et la carte existent
    user = User.query.get(user_id)
    card = Card.query.get(card_id)

    if not user or not card:
        return jsonify({"error": "Utilisateur ou carte non trouvée"}), 404

    # Vérifier si la carte est déjà dans la collection de l'utilisateur
    existing_entry = Collection.query.filter_by(user_id=user.id, card_id=card.id).first()
    
    if existing_entry:
        return jsonify({"error": "La carte est déjà dans la collection."}), 400

    # Ajouter la carte à la collection
    new_collection_entry = Collection(user_id=user.id, card_id=card.id)
    db.session.add(new_collection_entry)
    db.session.commit()

    return jsonify({"message": f"La carte {card.name} a été ajoutée à la collection de {user.username}."}), 200

@main.route('/wishlist/remove/<int:card_id>', methods=['POST'])
@login_required
def remove_from_wishlist(card_id):
    user = User.query.get(session["user_id"])
    card = Card.query.get(card_id)

    if not user or not card:
        return jsonify({"error": "Utilisateur ou carte non trouvée"}), 404

    wishlist_entry = Wishlist.query.filter_by(user_id=user.id, card_id=card.id).first()
    if wishlist_entry:
        db.session.delete(wishlist_entry)
        db.session.commit()
        return jsonify({"message": f"La carte {card.name} a été retirée de la wishlist."}), 200
    else:
        return jsonify({"message": "La carte n'est pas dans la wishlist."}), 200

@main.route('/wishlist')
@login_required
def get_wishlist():
    user = User.query.get(session["user_id"])
    wishlist = [{"id": card.id, "name": card.name} for card in user.wishlist]
    return jsonify(wishlist)

@main.route('/collection/<int:user_id>', methods=['GET'])
@login_required
def get_collection(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Utilisateur introuvable"}), 404

    # Récupérer les cartes de la collection avec une jointure
    collection_cards = (
        db.session.query(Card)
        .join(Collection, Card.id == Collection.card_id)
        .filter(Collection.user_id == user.id)
        .all()
    )

    collection_list = [{"id": card.id, "name": card.name} for card in collection_cards]
    
    return render_template('collection.html', collection=collection_list)

@main.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    card_type = request.args.get('type')

    if not query:
        return jsonify({"error": "Aucun terme de recherche fourni"}), 400

    query_filter = Card.query.filter(Card.name.ilike(f'%{query}%'))

    if card_type:
        query_filter = query_filter.filter(Card.type.ilike(f'%{card_type}%'))

    cards = query_filter.all()
    results = {
        "cards": [{"id": card.id, "name": card.name, "type": card.type} for card in cards]
    }

    return render_template('search.html', results=results, user_id=session.get("user_id"))
