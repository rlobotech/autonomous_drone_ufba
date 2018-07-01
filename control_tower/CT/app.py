# -*- coding: utf-8 -*-
# all the imports
from flask import Flask, request, flash, url_for, redirect, render_template, session, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_principal import identity_loaded, RoleNeed, UserNeed
from flask_paginate import Pagination
from flask_wtf import CSRFProtect
from datetime import datetime, timedelta
from CT.forms import *
from lib.functions import get_page_items, crypt, verify_crypt
import locale


# Global variables
attempts = 0 # variavel para o captcha

# App
app = Flask(__name__)
# Config
app.config.from_object('CT.config')
app.config.from_pyfile('config.cfg', silent=True)

# Enable CSRF protection globally for a Flask app
csrf = CSRFProtect(app)
csrf.init_app(app)

# Flask-SQLAlchemy
db = SQLAlchemy(app)

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Automatically create tables
from models import *
db.create_all()

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

################ Calculo das estatisticas ################
def calcule_statistics():
    total_drones = 0
    total_missions = 0
    drones = Drones.query.all()
    for drone in drones:
        total_drones += 1
    return total_drones

###########################################################
## Routers
###########################################################

@app.route('/', methods = ['GET', 'POST'])
@login_required
def dashboard():
    connect = 0
    drones = Drones.query.all()
    #SEARCH
    drone_search = ""
    if request.method == 'POST':
        drone_search = (request.form['drone_search']).strip()
        if drone_search:
            drones = Drones.query.filter(Drones.name.ilike('%'+drone_search+'%') | \
                                       Drones.model.ilike('%'+drone_search+'%')| \
                                       Drones.ip.ilike('%'+drone_search+'%'))
        # buttom connect
        #connect = request.form['status']

    total_drones = calcule_statistics()
    return render_template('dashboard.html', \
                           drones=drones, \
                           drone_search=drone_search, \
                           total_drones=total_drones, \
                           connect=connect  )



###########################################################
## Users
###########################################################

@app.route('/users/', methods = ['GET', 'POST'])
@login_required
def users():
    users = Users.query.all()
    #SEARCH
    user_search = ""
    if request.method == 'POST':
        user_search = (request.form['user_search']).strip()
        if user_search:
            users = Users.query.filter(Users.realname.ilike('%'+user_search+'%')| \
                                       Users.email.ilike('%'+user_search+'%'))
    return render_template('users.html', users=users, user_search=user_search)

@app.route('/user/new/')
@login_required
def user_new():
    form = UserForm()
    return render_template('user_new.html', form=form)

@app.route('/user/new/submit/', methods = ['POST'])
@login_required
def user_new_submit():
    form = UserForm()
    if form.validate_on_submit():
        password = form.password.data
        realname = form.realname.data
        email = (form.email.data).replace(" ", "")
        active = form.active.data

        user_email = Users.query.filter_by(email=request.form['email']).first()
        if user_email:
            return u"Esse e-mail já existe"
        else:
            user = Users(realname, password, email, active)
            db.session.add(user)
            db.session.commit()
            return "Usuario cadastrado com sucesso"
    else:
        return str(form.errors)

@app.route('/user/edit/<int:user_id>')
@login_required
def user_edit(user_id):
    user = Users.query.get(user_id)
    form = UserForm(obj=user)
    return render_template('user_edit.html', user=user, form=form)


@app.route('/user/edit/submit', methods=['POST'])
@login_required
def user_edit_submit():
    if request.method == 'POST':
        user_id = request.form['id']
        user = Users.query.get(user_id)
        form = UserForm()
        if form.validate_on_submit():
            user_email = Users.query.filter(Users.email == form.email.data,
                                            Users.id != user_id).first()
            if user_email:
                return u"Esse e-mail já existe"
            else:
                if form.password.data == "#########":
                    user.password = user.password
                else:
                    user.set_password(form.password.data)
                user.realname = form.realname.data
                user.email = (form.email.data).replace(" ", "")
                user.active = form.active.data
                db.session.commit()
                return "Usuario editado com sucesso"
        else:
            return str(form.errors)


@app.route('/user/delete/', methods=['POST'])
@login_required
def user_delete():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user = Users.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('users'))

@app.route('/config/account', methods=['GET', 'POST'])
@login_required
def config_account():
    user = Users.query.get(current_user.id)
    form = PerfilForm(formdata=None, obj=user)
    form2 = PerfilSenhaForm()
    return render_template('account.html', form=form, form2=form2)


@app.route('/config/account/edit', methods=['POST'])
@login_required
def config_account_edit():
    form = PerfilForm()
    if form.validate_on_submit():
        email = (form.email.data).replace(" ", "")

        verify_email = Users.query.filter(Users.email == email,
                                          Users.id != current_user.id).first()
        if verify_email:
            return u"E-mail já existe"

        user = Users.query.get(current_user.id)
        user.realname = form.realname.data
        user.email = email
        db.session.commit()
        return "Conta alterada com sucesso"
    else:
        return str(form.errors)


@app.route('/config/account/password', methods=['POST'])
@login_required
def config_account_password():
    form = PerfilSenhaForm()
    if form.validate_on_submit():
        password_one = form.password_one.data
        password_two = form.password_two.data

        user = Users.query.get(current_user.id)
        if user.verify_password(password_one):
            user.set_password(password_two)
            db.session.commit()
            return "Senha alterada com sucesso"
        else:
            return "Senha antiga não conferem!"
    else:
        return str(form.errors)

###########################################################
## Drones
###########################################################

@app.route('/drones/', methods = ['GET', 'POST'])
@login_required
def drones():
    drones = Drones.query.all()
    #SEARCH
    drone_search = ""
    if request.method == 'POST':
        drone_search = (request.form['drone_search']).strip()
        if drone_search:
            drones = Drones.query.filter(Drones.name.ilike('%'+drone_search+'%') | \
                                       Drones.model.ilike('%'+drone_search+'%')| \
                                       Drones.ip.ilike('%'+drone_search+'%'))
    return render_template('drones.html', drones=drones, drone_search=drone_search)

@app.route('/drone/new/')
@login_required
def drone_new():
    form = DroneForm()
    return render_template('drone_new.html', form=form)

@app.route('/drone/new/submit/', methods = ['POST'])
@login_required
def drone_new_submit():
    form = DroneForm()
    if form.validate_on_submit():
        name = form.name.data
        model = form.model.data
        ip = form.ip.data

        drone_name = Drones.query.filter_by(name=name).first()
        drone_ip = Drones.query.filter_by(ip=ip).first()
        if drone_name:
            return u"Esse nome do drone já existe"
        elif drone_ip:
            return u"Esse ip já existe"
        else:
            drone = Drones(name, model, ip)
            db.session.add(drone)
            db.session.commit()
            return "Drone cadastrado com sucesso"
    else:
        return str(form.errors)

@app.route('/drone/edit/', methods=['POST'])
@login_required
def drone_edit():
    if request.method == 'POST':
        drone_id = request.form['id']
        drone = Drones.query.get(drone_id)
        form = DroneForm(formdata=None, obj=drone)
        return render_template('drone_edit.html', drone=drone, form=form)

@app.route('/drone/edit/submit/', methods=['POST'])
@login_required
def drone_edit_submit():
    if request.method == 'POST':
        drone_id = request.form['id']
        drone = Drones.query.get(drone_id)

        form = DroneForm()
        if form.validate_on_submit():
            drone_name = Drones.query.filter(Drones.name==form.name.data, Drones.id!=drone_id).first()
            drone_ip = Drones.query.filter(Drones.ip==form.ip.data, Drones.id!=drone_id).first()
            if drone_name:
                return u"Esse nome de drone já existe"
            elif drone_ip:
                return u"Esse ip já existe"
            else:
                drone.name = form.name.data
                drone.model = form.model.data
                drone.ip = form.ip.data
                db.session.commit()
                return "Drone editado com sucesso"
        else:
            return str(form.errors)

@app.route('/drone/delete/', methods=['POST'])
@login_required
def drone_delete():
    if request.method == 'POST':
        drone_id = request.form['id']
        drone = Drones.query.get(drone_id)
        db.session.delete(drone)
        db.session.commit()
        return redirect(url_for('drones'))

###########################################################
## Missions
###########################################################

@app.route('/missions/', methods = ['GET', 'POST'])
@login_required
def missions():
    missions = Missions.query.all()
    #SEARCH
    mission_search = ""
    if request.method == 'POST':
        mission_search = (request.form['mission_search']).strip()
        if mission_search:
            missions = Missions.query.filter(Missions.name.ilike('%'+mission_search+'%'))
    return render_template('missions.html', missions=missions, mission_search=mission_search)

@app.route('/mission/new/')
@login_required
def mission_new():
    form = MissionForm()
    return render_template('mission_new.html', form=form)

@app.route('/mission/new/submit/', methods = ['POST'])
@login_required
def mission_new_submit():
    form = MissionForm()
    if form.validate_on_submit():
        name = form.name.data
        coordinates = request.form['coordinates']
        print coordinates[0]
        mission_name = Missions.query.filter_by(name=name).first()
        if mission_name:
            return u"Missao ja existe"
        else:
            mission = Missions(name, coordinates)
            db.session.add(mission)
            db.session.commit()
            return u"Missao cadastrada com sucesso"
    else:
        return str(form.errors)

@app.route('/mission/edit/', methods=['POST'])
@login_required
def mission_edit():
    if request.method == 'POST':
        mission_id = request.form['id']
        mission = Missions.query.get(mission_id)
        form = MissionForm(formdata=None, obj=mission)
        return render_template('mission_edit.html', mission=mission, form=form)

@app.route('/mission/edit/submit/', methods=['POST'])
@login_required
def mission_edit_submit():
    if request.method == 'POST':
        mission_id = request.form['id']
        mission = Missions.query.get(mission_id)

        form = MissionForm()
        if form.validate_on_submit():
            mission_name = Mission.query.filter(Mission.name==form.name.data, Mission.id!=mission_id).first()
            if mission_name:
                return u"Esse nome já existe"
            else:
                mission.name = form.name.data
                mission.model = form.model.data
                db.session.commit()
                return "Missão editada com sucesso"
        else:
            return str(form.errors)

@app.route('/mission/delete/', methods=['POST'])
@login_required
def mission_delete():
    if request.method == 'POST':
        mission_id = request.form['id']
        mission = Missions.query.get(mission_id)
        db.session.delete(mission)
        db.session.commit()
        return redirect(url_for('missions'))

##########################################################
## GPS - mapeamento
##########################################################

@app.route('/map/', methods=['GET', 'POST'])
@login_required
def map():
    All = 1
    drones = Drones.query.all()
    if request.method == 'POST':
        drone_id = request.form['id']
        drones = Drones.query.get(drone_id)
        if drones:
            All = 0
            return render_template('map.html', drones=drones, All=All)
    return render_template('map.html', drones=drones, All=All)

##########################################################
## Leitura dos sensores
##########################################################

@app.route('/sensors/', methods=['GET', 'POST'])
@login_required
def sensors():
    All = 1
    drones = Drones.query.all()
    if request.method == 'POST':
        drone_id = request.form['id']
        drones = Drones.query.get(drone_id)
        if drones:
            All = 0
            return render_template('sensors.html', drones=drones, All=All)
    return render_template('sensors.html', drones=drones, All=All)

##########################################################
## Controlador manual
##########################################################

@app.route('/controller/', methods=['GET', 'POST'])
@login_required
def controller():
    All = 1
    drones = Drones.query.all()
    if request.method == 'POST':
        drone_id = request.form['id']
        drones = Drones.query.get(drone_id)
        if drones:
            All = 0
            return render_template('controller.html', drones=drones, All=All)
    return render_template('controller.html', drones=drones, All=All)

##########################################################
## Login
##########################################################

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))


# User login methods
@login_manager.user_loader
def user_loader(user_id):
    return Users.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login'))

def login_attempts_count():
    time_range = datetime.now() - timedelta(minutes=60)
    attempts = LoginLogging.query.filter(
                                LoginLogging.ip_address == request.remote_addr,
                                LoginLogging.datetime > time_range,
                                LoginLogging.success == False).count()
    return attempts

@app.route('/login/', methods=['GET', 'POST'])
def login():
    ignore_captcha = login_attempts_count() <= 2
    form = LoginForm(ignore_captcha)

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and user.active and user.verify_password(form.password.data):
            # Keep the user info in the session using Flask-Login
            login_user(user)

            login_log = LoginLogging(request.remote_addr,
                                     form.email.data, True)
            user.set_last_login(request.remote_addr)
            db.session.add(login_log)
            db.session.commit()
            return redirect(url_for('dashboard'))
        else:
            login_log = LoginLogging(request.remote_addr,
                                     form.email.data, False)
            db.session.add(login_log)
            db.session.commit()
            flash(u'Usuário ou senha inválidos', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout/')
@login_required
def logout():
    # Remove the user information from the session
    logout_user()
    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    return redirect(url_for('login'))

###################################
## Filters
###################################
@app.template_filter('format_currency')
def format_currency(value):
    if not value:
        return ''
    locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
    return locale.currency(value, grouping=True)
