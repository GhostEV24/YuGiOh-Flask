from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class RegisterForm(FlaskForm):
    username = StringField("Nom d'utilisateur", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    confirm_password = PasswordField("Confirmer le mot de passe", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("S'inscrire")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    submit = SubmitField("Se connecter")

class CardForm(FlaskForm):
    name = StringField("Nom de la carte", validators=[DataRequired()])
    description = StringField("Description")
    type = StringField("Type de carte", validators=[DataRequired()])
    attack = StringField("Points d'attaque")
    defense = StringField("Points de défense")
    submit = SubmitField("Ajouter la carte")
