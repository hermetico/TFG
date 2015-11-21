# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo


class LoginForm(Form):
    username = StringField(u"Usuario", validators=[DataRequired()])
    password = PasswordField(u"Contraseña", validators=[DataRequired()])
    remember_me = BooleanField('Recuerdame')
    submit = SubmitField(u"Validar")


class NewUserForm(Form):
    user = StringField(u"Usuario", validators=[DataRequired(), Length(1, 64),
                                               Regexp('^[A-Za-z][A-Za-z0-9]*$', 0, 'El nombre de usuario solo puede contener letras y numeros')])

    password = PasswordField(u"Contraseña", validators=[DataRequired(), EqualTo('password2', message='Las contraseñas deben coincidir')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField(u"Registrar")