"""
Formulaire de configuration d'un quizz
===================================================
    type de quizz : texte | proposition | notation
    -----------------------------------------------
    Nom de quizz => pour l'url
    Date de début du quizz
    Date de fin du quizz (15jours max)
    Texte de présentation du quizz
    Email organisateur
    => Generation d'un code
"""
from wtforms import StringField, validators, EmailField, PasswordField

from home.controller.frm import MFlaskForm


class FLogin(MFlaskForm):
    login = StringField('identifiant de connexion', validators=[validators.DataRequired()])
    password = PasswordField('Mot de passe', validators=[validators.DataRequired()])


class FSignin(MFlaskForm):
    login = StringField('identifiant de connexion', validators=[validators.DataRequired()])
    email = EmailField('Adresse electronique', validators=[validators.DataRequired()])
    name = StringField('Nom', validators=[validators.DataRequired()])
    password = PasswordField('Mot de passe', validators=[validators.DataRequired()])
    confirm = PasswordField('Confirmer mot de passe', validators=[validators.DataRequired()])
