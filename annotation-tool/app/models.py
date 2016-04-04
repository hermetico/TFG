# -*- coding: utf-8 -*-
from . import db
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128), index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    pictures = db.relationship('Picture', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @property
    def is_admin(self):
        return self.role_id == 1

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

    def fancy_print(self):
        print """User:
        \tid: %(id)s
        \tusername: %(name)s
        \trole: %(role)s""" % (
            dict(id=self.id, name=self.username, role=self.role_id)
        )

    @property
    def num_pictures(self):
        """Return the number of pictures associated with the user"""
        return self.pictures.count()


class Picture(db.Model):
    __tablename__ = 'pictures'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    date = db.Column(db.DateTime, index=True)
    path = db.Column(db.String(256))
    label_id = db.Column(db.Integer, db.ForeignKey('labels.id'), index=True)
    comment = db.Column(db.String(256), default='')


    def __repr__(self):
        """
        :return:default representation for the current model
        """
        return "<Picture id: %(id)s>"% dict(id=self.id)

    def fancy_print(self):
        print """Picture
        \tid = %(id)s
        \tuserid = %(userid)s
        \tdate = %(date)s
        \tpath = %(path)s
        \tlabelid = %(labelid)s """ % (
            dict(id=self.id,
                 userid=self.user_id,
                 date=self.date,
                 path=self.path,
                 labelid=self.label_id,
                 comment=self.comment)
        )


class Label(db.Model):
    __tablename__ = 'labels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    pictures = db.relationship('Picture', backref='label', lazy='dynamic')

    def __repr__(self):
        return '<Label %r>' % self.name