# -*- coding: utf-8 -*-

"""
Author : Mildred Fakoya
Date : March 9, 2021

"""
import os

# Import flask and its modules needed for the functionalities of this page

from flask import (
    Flask,
    render_template,
    flash,
    redirect,
    request,
    session,
    logging,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm import backref
from forms import LoginForm, RegisterForm
from Crypto.Cipher import AES
from helpers.encryption import AESEncrpytion
from config import DevelopmentConfig
from dotenv import load_dotenv
from models import Users, UserEncryption
from flask_migrate import Migrate

load_dotenv(".env")
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy()
migrate = Migrate()
db.init_app(app)
migrate.init_app(app, db)

"""
CREATE THE ROUTES TO THE INDEX PAGE, THE LOGIN PAGE AND THE REGISTER PAGE
note to self : Take the registration to the administrative module
"""


@app.route("/")
def home():
    return render_template("index.html")


# User Registration API Endpoint
@app.route("/register/", methods=["GET", "POST"])
def register():
    # Creating RegistrationForm class object
    form = RegisterForm(request.form)
    # Cheking that method is post and form is valid or not.
    if request.method == "POST" and form.validate():
        encrypted_email = AESEncrpytion().encrypt(UserEncryption, form.email.data)
        encrypted_password = AESEncrpytion().encrypt(UserEncryption, form.password.data)

        # create new user model object
        new_user = Users(
            user_id=form.user_id.data,
            user_email=form.email.data,
            user_first_name_encrypted=AESEncrpytion()
            .encrypt(UserEncryption, form.firstname.data)
            .id,
            user_middle_name_encrypted=AESEncrpytion()
            .encrypt(UserEncryption, form.middlename.data)
            .id,
            user_last_name_encrypted=AESEncrpytion()
            .encrypt(UserEncryption, form.lastname.data)
            .id,
            # role=form.role.data,
            user_email_encrypted=encrypted_email.id,
            user_password_encrypted=encrypted_password.id,
        )
        # saving user object into data base with hashed password
        db.session.add(new_user)
        db.session.commit()
        flash("You have successfully registered", "success")
        # if registration successful, then redirecting to login Api
        return redirect(url_for("login"))
    else:
        # if method is Get, than render registration form
        return render_template("register.html", form=form)
    # Login API endpoint implementation


@app.route("/login/", methods=["GET", "POST"])
def login():
    # Creating Login form object
    form = LoginForm(request.form)
    # verifying that method is post and form is valid
    if request.method == "POST" and form.validate:
        # checking that user is exist
        try:
            user = Users.query.filter_by(user_email=form.email.data).one()
        except (NoResultFound, MultipleResultsFound) as e:
            flash("Invalid email or password", "danger")
            return redirect(url_for("login"))

        decrypted_password = AESEncrpytion().decrypt(
            UserEncryption, user.user_password_encrypted
        )
        # if user exist in database than we will compare our database hased password and password come from login form
        if form.password.data != decrypted_password:
            flash("Invalid email or password", "danger")
            return redirect(url_for("login"))

        # if password is matched, allow user to access and save email and username inside the session
        flash("You have successfully logged in.", "success")
        session["logged_in"] = True
        session["user_email"] = user.user_email
        # After successful login, redirecting to home page
        return redirect(url_for("home"))

    # rendering login page
    return render_template("login.html", form=form)


@app.route("/logout/")
def logout():
    # Removing data from session by setting logged_flag to False.
    session["logged_in"] = False
    # redirecting to home page
    return redirect(url_for("home"))


if __name__ == "__main__":
    # Creating database tables
    db.create_all()
    # running server
    app.run(host="0.0.0.0")
