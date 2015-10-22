# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, url_for, flash, g
from flask.ext.login import login_user, current_user
from flask.ext.login import logout_user, login_required
from . import auth
from ..models import User
from .forms import LoginForm
from .. import login_manager




@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # pueden haber varios users con el mismo nombre
        users = User.query.filter_by(username=form.username.data).all()
        if users is not None:
            for user in users:
                if user.verify_password(form.password.data):
                    login_user(user, form.remember_me.data)
                    flash('Bienvenido/a %s' %user.username , 'success')
                    return redirect(request.args.get('next') or url_for('main.index'))
        flash('Usuario y/o contraseña incorrectos.', 'danger')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    flash('Hasta pronto %s!' % current_user.username, 'success')
    logout_user()
    return redirect(url_for('.login'))


