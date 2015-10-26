# -*- coding: utf-8 -*-
from flask import render_template, session, redirect, url_for, flash, json, Response
from flask.ext.login import login_required
from .decorators import admin_required
from . import main
from .. import db
from ..models import User, Label, Picture, Role
from .forms import NewUserForm, NewLabelForm


@main.context_processor
def current_user():
    users_with_pictures = db.session.query(User.username, User.id).filter(User.role_id!=1).all()
    users_with_pictures = [{'username': x[0], 'id':x[1]} for x in users_with_pictures]
    return dict(users_with_pictures=users_with_pictures)

@main.route('/')
def index():
    return redirect(url_for('main.main_page'))


@main.route('/main')
@login_required
def main_page():
    return render_template('index.html')


@main.route('/users', methods=['GET', 'POST'])
@login_required
@admin_required
def users():
    form = NewUserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            flash('Ya existe un usuario llamado %s' % user.username, 'danger')
            return redirect(url_for('.users'))
        user = User(username=form.username.data, password=form.password.data, role_id=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('Usuario %s registrado correctamente' %user.username, 'success')
        return redirect(url_for('.users'))
    user_list = User.query.order_by(User.id).all()
    return render_template('users.html', form=form, users=user_list)


@main.route('/labels', methods=['GET', 'POST'])
@login_required
@admin_required
def labels():
    form = NewLabelForm()
    if form.validate_on_submit():
        label = Label.query.filter_by(name=form.label.data).first()
        if label is not None:
            flash('La etiqueta %s ya existe' % label.name, 'danger')
            return redirect(url_for('.labels'))
        label = Label(name=form.label.data)
        db.session.add(label)
        db.session.commit()
        flash('Etiqueta  %s registrada correctamente' %label.name, 'success')
        return redirect(url_for('.labels'))

    label_list = Label.query.order_by(Label.id).all()
    return render_template('labels.html', form=form, labels=label_list)


@main.route('/catalog/<int:userid>')
@login_required
def cataloguser(userid):
    user = User.query.filter_by(id=userid).first()
    if user is not None:
        label = 'year'
        rows = db.session.query(db.func.strftime('%Y', Picture.date).label(label))\
                .filter(Picture.user_id==user.id).group_by(label).all()
        rows = [x[0] for x in rows]

        baseurl = url_for('.cataloguser', userid=userid)
        if not rows:
            flash('El usuario %s no tiene imagenes asociadas' % user.username, 'info')
            return redirect(url_for('.index'))
        return render_template('catalog.html', data={'label': 'Año', 'rows': rows, 'baseurl': baseurl})
    flash('El usuario especificado no existe', 'info')
    return redirect(url_for('.index'))


@main.route('/catalog/<int:userid>/<year>')
@login_required
def catalogyear(userid, year):
    user = User.query.filter_by(id=userid).first()
    label = 'month'
    if user is not None and len(year)==4:
        rows = db.session.query(db.func.strftime('%m', Picture.date).label(label))\
            .filter(Picture.user_id==user.id).filter(db.func.strftime('%Y', Picture.date)==year)\
            .group_by(label).all()
        rows = [x[0] for x in rows]
        baseurl = url_for('.catalogyear', userid=userid, year=year)
        if not rows:
            flash('El usuario %s no tiene imagenes asociadas para esta combinacion de fechas' % user.username, 'info')
            return redirect(url_for('.index'))
        return render_template('catalog.html', data={'label': 'Mes', 'rows': rows, 'baseurl': baseurl})
    flash('El usuario especificado no existe', 'info')
    return redirect(url_for('.index'))



@main.route('/catalog/<int:userid>/<year>/<month>')
@login_required
def catalogmonth(userid, year, month):
    user = User.query.filter_by(id=userid).first()
    label = 'day'
    if user is not None and len(year)==4 and len(month)==2:
        rows = db.session.query(db.func.strftime('%d', Picture.date).label(label))\
            .filter(Picture.user_id==user.id).filter(db.func.strftime('%Y', Picture.date)==year)\
            .filter(db.func.strftime('%m', Picture.date)==month)\
            .group_by(label).all()
        rows = [x[0] for x in rows]
        baseurl = url_for('.catalogmonth', userid=userid, year=year, month=month)
        if not rows:
            flash('El usuario %s no tiene imagenes asociadas para esta combinacion de fechas' % user.username, 'info')
            return redirect(url_for('.index'))
        return render_template('catalog.html', data={'label': 'Dia', 'rows': rows, 'baseurl': baseurl})
    flash('El usuario especificado no existe', 'info')
    return redirect(url_for('.index'))

@main.route('/catalog/<int:userid>/<year>/<month>/<day>')
@main.route('/catalog/<int:userid>/<year>/<month>/<day>/<int:labelid>')
@login_required
def catalogday(userid, year, month, day, labelid=1):
    date = '%s-%s-%s' %(year, month, day)
    user = User.query.filter_by(id=userid).first()
    numpictures = Picture.query.filter(Picture.user_id==user.id)\
                    .filter(db.func.strftime('%Y-%m-%d', date)\
                    ==db.func.strftime('%Y-%m-%d', Picture.date)).count()
    if user is not None and numpictures:
        label_list = Label.query.order_by(Label.id).all()
        return render_template('api-catalog.html', data={'date':date, 'labelid':labelid,
            'userid':user.id, 'labels':label_list})

    flash('El usuario %s no tiene imagenes asociadas para esta combinacion de fechas' % user.username, 'info')
    return redirect(url_for('.index'))


@main.route('/api/get/<int:userid>/<date>')
@main.route('/api/get/<int:userid>/<date>/<int:labelid>/<int:page>')
@login_required
def apiget(userid, date, page=1, labelid=1):
    pagesize = 10
    pictures = Picture.query.filter(Picture.user_id==userid)\
                .filter(db.func.strftime('%Y-%m-%d', date)==db.func.strftime('%Y-%m-%d', Picture.date))\
                .filter(Picture.label_id==labelid)\
                .paginate(page, pagesize, False).items
    nextpage = page + 1
    # basic response structure
    result = {'working': True, 'next-page': nextpage, 'label-id': labelid, 'user-id': userid}
    pictures = { picture.id : {'path': picture.path, 'label': picture.label_id, 'id': picture.id} for picture in pictures}
    result['pictures'] = pictures
    # dumping data
    js = json.dumps(result)
    resp = Response(js, status=200, mimetype='application/json')
    return resp