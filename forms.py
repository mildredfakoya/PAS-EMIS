# -*- coding: utf-8 -*-
"""
Author : Mildred Fakoya
Date : March 9, 2021
"""

#USERS LOGIN and REGISTRATION FORM
 
from wtforms import Form, StringField, PasswordField, BooleanField,  SelectField,  validators
from wtforms.validators import DataRequired as Required


# LOGIN FORM
class LoginForm(Form):
    email = StringField("Email", validators=[validators.Length(min=7, max=50), Required(message="Please Fill This Field")])
    password = PasswordField("Password", validators=[Required(message="Please Fill This Field")])

# Creating Registration Form contains username, name, email, password and confirm password.

class RegisterForm(Form):
    
    user_id = StringField("User ID", validators=[validators.Length(min=7, max=20)])
    firstname = StringField("First Name", validators=[validators.Length(min=3, max=50), Required(message="First Name is required")])
    middlename = StringField("Middle Name", validators=[validators.Length(min=3, max=50)])
    lastname = StringField("Last Name", validators=[validators.Length(min=3, max=50), Required(message="Last Name is required")])
    email = StringField("Email", validators=[validators.Email(message="Please enter a valid email address")])
    password = PasswordField("Password", validators=[

        validators.DataRequired(message="Please Fill This Field"),

        validators.EqualTo(fieldname="confirm", message="Your Passwords Do Not Match")
    ])

    confirm = PasswordField("Confirm Password", validators=[validators.DataRequired(message="Please Fill This Field")])

    #role = SelectField("Role", choices=['system administrator', 'school administrator'], validators=[validators.DataRequired(message="Please select a role")])
    
