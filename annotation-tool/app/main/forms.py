# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo

class NewUserForm(Form):
    username = StringField(u"Usuario", validators=[DataRequired(), Length(1, 64),
                                               Regexp('^[A-Za-z][A-Za-z0-9]*$', 0, 'El nombre de usuario solo puede contener letras y numeros')])

    password = PasswordField(u"Contraseña", validators=[DataRequired(), EqualTo('password2', message='Las contraseñas deben coincidir')])
    password2 = PasswordField(u'Confirmar contraseña', validators=[DataRequired()])
    role = SelectField(u'Rol', choices=[('1', 'Administrador'), ('2', 'Usuario')])

    submit = SubmitField(u"Registrar")

class NewLabelForm(Form):
     label = StringField(u"Nombre", validators=[DataRequired()])
     submit = SubmitField(u"Registrar")
