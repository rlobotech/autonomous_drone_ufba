# -*- coding: utf-8 -*-
from app import db
from flask_login import UserMixin
from bcrypt import hashpw, gensalt
from datetime import datetime


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    realname = db.Column(db.String)
    password = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    last_login_ip = db.Column(db.String)
    last_login_date = db.Column(db.DateTime)
    active = db.Column(db.Boolean)

    def __init__(self, realname, password, email, active):
        self.realname = realname
        self.email = email
        self.active = active
        self.set_password(password)

    def __repr__(self):
        return '<User %s>' % self.email

    def set_password(self, password):
        salt = gensalt(8)
        self.password = hashpw(password, salt)

    def verify_password(self, password_to_check):
        return hashpw(password_to_check, self.password) == self.password

    def set_last_login(self, ip_address):
        self.last_login_ip = ip_address
        self.last_login_date = datetime.now()

class Drones(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    model = db.Column(db.String)
    ip = db.Column(db.String, unique=True)

    def __init__(self, name, model, ip):
        self.name = name
        self.model = model
        self.ip = ip

    def __repr__(self):
        return '<Drone %s>' % self.name

class Missions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    coordinates = db.Column(db.String)

    def __init__(self, name, coordinates):
        self.name = name
        self.coordinates = coordinates

    def __repr__(self):
        return '<Missions %s>' % self.name

class LoginLogging(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip_address = db.Column(db.String)
    login = db.Column(db.String)
    datetime = db.Column(db.DateTime)
    success = db.Column(db.Boolean)

    def __init__(self, ip_address, login, success):
        self.ip_address = ip_address
        self.login = login
        self.success = success
        self.datetime = datetime.now()

    def __repr__(self):
        return '<LoginLogging %s %s %s>' % (self.ip_address,
                                            self.login, self.datetime)
