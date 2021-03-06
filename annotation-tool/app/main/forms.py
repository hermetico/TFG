# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, SelectField, IntegerField, SelectMultipleField, widgets
from wtforms import BooleanField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo

class ChoiceObj(object):
    def __init__(self, name, choices):
        # this is needed so that BaseForm.process will accept the object for the named form,
        # and eventually it will end up in SelectMultipleField.process_data and get assigned
        # to .data
        setattr(self, name, choices)

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.TableWidget()
    option_widget = widgets.CheckboxInput()

    # uncomment to see how the process call passes through this object
    #def process_data(self, value):
    #    return super(MultiCheckboxField, self).process_data(value)


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

class EliminarImagenesSinEtiqueta(Form):
     clave = StringField(u"Escribe la palabra 'eliminar'")
     eliminar = SubmitField(u"Eliminar")

class EliminarImagenesYEtiquetas(Form):
     clave = StringField(u"Escribe la palabra 'eliminar-todo'")
     limpiar = SubmitField(u"Eliminar")

class ImportarImagenes(Form):
     clave = StringField(u"Escribe la palabra 'eliminar-todo'")
     importar = SubmitField(u"Eliminar")

class CreateDatasetForm(Form):
    append_path = StringField(u"Añadir path en train/test txt")
    use_local_abs_path = BooleanField(u"Usar path absoluto del servidor", default=False)
    shuffle_images = BooleanField(u"De volver imagenes con orden aleatorio", default=False)
    validation_percent = IntegerField(u"Porcentaje de imagenes para validation", default=0)
    test_percent = IntegerField(u"Porcentaje de imagenes para test", default=0)
    limit_class = IntegerField(u"Limitar el numero de imagenes por classe", default=0)
    select_labels = MultiCheckboxField(None)
