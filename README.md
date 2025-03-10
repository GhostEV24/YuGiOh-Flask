﻿# Mon Projet Yu-Gi-Oh
Yu-Gi-Oh! Card Manager

Ce projet est une application Flask permettant de gérer une collection de cartes Yu-Gi-Oh! et une wishlist.

Prérequis

1. Dépendances

Assurez-vous d'avoir installé :

Python 3.x

Flask et ses dépendances

Docker (utilisé uniquement pour MySQL)

MySQL (exécuté via Docker)

2. Installation des dépendances

Créez un environnement virtuel et installez les dépendances :

python -m venv venv
source venv/bin/activate  # Sur macOS/Linux
venv\Scripts\activate    # Sur Windows
pip install -r requirements.txt

Configuration de la base de données

Lancer MySQL avec Docker

docker run --name mysql-yugioh -e MYSQL_ROOT_PASSWORD=rootpassword -e MYSQL_DATABASE=yugioh -e MYSQL_USER=flaskuser -e MYSQL_PASSWORD=flaskpassword -p 3306:3306 -d mysql:latest

Configurer l'URI SQLAlchemy (dans config.py) :

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://flaskuser:flaskpassword@localhost/yugioh'

Initialiser la base de données :

flask db init
flask db migrate -m "Initial migration"
flask db upgrade

Lancer l'application

flask run

L'application sera disponible à l'adresse : http://127.0.0.1:5000

Fonctionnalités principales

Inscription & Connexion

Ajout & Suppression de cartes dans la collection

Ajout & Suppression de cartes dans la wishlist

Recherche de cartes via l'API Yu-Gi-Oh!

Déploiement

Pour pousser ce projet sur GitHub :

git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/votre-utilisateur/votre-repo.git
git push -u origin main

Remarque

Pensez à modifier les identifiants MySQL pour un environnement de production.

