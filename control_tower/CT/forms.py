# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.recaptcha.validators import Recaptcha
from wtforms import (
    IntegerField,
    SelectMultipleField,
    StringField,
    PasswordField,
    TextAreaField,
    SelectField,
    HiddenField,
    RadioField,
    BooleanField)
from wtforms.widgets.html5 import *
from wtforms.fields.html5 import *
from wtforms.validators import (
        DataRequired,
        EqualTo,
        InputRequired,
        StopValidation)

class UserForm(FlaskForm):
    realname = StringField(u'Nome Completo', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    email = EmailField('E-mail', validators=[DataRequired()])
    active = SelectField(u'Conta',
                         choices=[(True, 'Ativa'), (False, 'Inativa')],
                         coerce=lambda x: x == 'True',
                         validators=[InputRequired()])

def validate_ignore_captcha(form, field):
    if form.ignore_captcha:
        raise StopValidation()

class LoginForm(FlaskForm):
    email = EmailField('E-mail:', validators=[DataRequired()])
    password = PasswordField('Senha:', validators=[DataRequired()])
    recaptcha = RecaptchaField(validators=[validate_ignore_captcha, Recaptcha()])

    def __init__(self, ignore_captcha=False):
        super(LoginForm, self).__init__()
        self.ignore_captcha = ignore_captcha

class PerfilForm(FlaskForm):
    realname = StringField(u'Nome Completo', validators=[DataRequired()])
    email = EmailField('E-mail', validators=[DataRequired()])
    email_two = EmailField('Confirmar E-mail',
                           validators=[DataRequired(), EqualTo('email')])


class PerfilSenhaForm(FlaskForm):
    password_one = PasswordField(u'Senha antiga', validators=[DataRequired()])
    password_two = PasswordField(u'Senha Nova', validators=[DataRequired()])
    password_three = PasswordField(u'Confirmar senha',
                                   validators=[DataRequired(),
                                               EqualTo('password_two')])

class DroneForm(FlaskForm):
    name = StringField(u'Identifição:', validators=[DataRequired()])
    model = StringField('Modelo', validators=[DataRequired()])
    ip = StringField(u'Endereço IP', validators=[DataRequired()])
    mission = SelectField(u'Missão',
                           choices=[('', 'Selecione...'),
                                    (1, 'PAF5'),
                                    (2, 'STI'),
                                    (3, 'As gordinhas de ondina')],
                           validators=[DataRequired()])
    emergency = SelectField(u'Emergência', choices=[(True, 'Ativa'), (False, 'Inativa')],
                         coerce=lambda x: x == 'True',
                         validators=[InputRequired()])

class MissionForm(FlaskForm):
    name = StringField(u'Nome da missão:', validators=[DataRequired()])
