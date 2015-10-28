# -*- coding: utf-8 -*-
from flask import render_template, session, redirect, url_for, flash, json, Response, request
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


#################################################
## Rutas del catalogo
#################################################

# es el primer paso del catalogo, muestra los años
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
        breadcrumb = [{'text': 'catalogo', 'url': '/catalog/%i' % userid}]

        return render_template('catalog.html', data={'label': 'Año', 'rows': rows, 'baseurl': baseurl},
                               breadcrumbs=breadcrumb)
    flash('El usuario especificado no existe', 'info')
    return redirect(url_for('.index'))


# segundo paso del catalogo muestra los meses
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
        breadcrumb = [
            {'text': 'catalogo', 'url': '/catalog/%i' % userid},
            {'text': year, 'url': '/catalog/%i/%s' %(userid, year)}
        ]
        return render_template('catalog.html', data={'label': 'Mes', 'rows': rows, 'baseurl': baseurl},
                               breadcrumbs=breadcrumb)
    flash('El usuario especificado no existe', 'info')
    return redirect(url_for('.index'))


# tercer paso del catalogo muestra los dias
@main.route('/catalog/<int:userid>/<year>/<month>')
@login_required
def catalogmonth(userid, year, month):
    user = User.query.filter_by(id=userid).first()
    label = 'day'

    # nos aseguramos que hay user, que el año tiene cuatro letras y el mes 2
    if user is not None and len(year)==4 and len(month)==2:
        rows = db.session.query(db.func.strftime('%d', Picture.date).label(label))\
            .filter(Picture.user_id==user.id).filter(db.func.strftime('%Y', Picture.date)==year)\
            .filter(db.func.strftime('%m', Picture.date)==month)\
            .group_by(label).all()
        rows = [x[0] for x in rows]
        baseurl = url_for('.catalogmonth', userid=userid, year=year, month=month)
        label_list = Label.query.order_by(Label.id).all()
        if not rows:
            flash('El usuario %s no tiene imagenes asociadas para esta combinacion de fechas' % user.username, 'info')
            return redirect(url_for('.index'))
        breadcrumb = [
            {'text': 'catalogo', 'url': '/catalog/%i' % userid},
            {'text': year, 'url': '/catalog/%i/%s' %(userid, year)},
            {'text': month, 'url': '/catalog/%i/%s/%s' %(userid, year, month)}
        ]
        return render_template('catalog.html', data={'label': 'Dia', 'rows': rows, 'baseurl': baseurl, 'label-list': label_list},
                               breadcrumbs=breadcrumb)
    flash('El usuario especificado no existe', 'info')
    return redirect(url_for('.index'))

## recibe la fecha y el label(opcional) y reenvia a la pagina de la api
@main.route('/catalog/<int:userid>/<year>/<month>/<day>')
@main.route('/catalog/<int:userid>/<year>/<month>/<day>/<int:labelid>')
@login_required
def catalogday(userid, year, month, day, labelid=None):
    date = '%s-%s-%s' %(year, month, day)
    user = User.query.filter_by(id=userid).first()
    numpictures = Picture.query.filter(Picture.user_id==user.id)\
                    .filter(db.func.strftime('%Y-%m-%d', date)\
                    ==db.func.strftime('%Y-%m-%d', Picture.date)).count()
    if user is not None and numpictures:
        label_list = Label.query.order_by(Label.id).all()

        breadcrumb = [
            {'text': 'catalogo', 'url': '/catalog/%i' % userid},
            {'text': year, 'url': '/catalog/%i/%s' %(userid, year)},
            {'text': month, 'url': '/catalog/%i/%s/%s' %(userid, year, month)}
        ]
        # dependiendo de si han especificado o no label, lo mostramos en el breadcrumb o no
        if labelid is not None:
            label_name = Label.query.filter_by(id=labelid).first().name
            breadcrumb.append({'text': '%s - %s'%(day, label_name), 'url': '/catalog/%i/%s/%s/%s/%s' %(userid, year, month, day, labelid)})
        else:
            breadcrumb.append({'text': '%s'%(day), 'url': '/catalog/%i/%s/%s/%s' %(userid, year, month, day)})

        return render_template('api-catalog.html', data={'date':date, 'labelid':labelid,
            'userid':user.id, 'labels':label_list}, breadcrumbs=breadcrumb)

    flash('El usuario %s no tiene imagenes asociadas para esta combinacion de fechas' % user.username, 'info')
    return redirect(url_for('.index'))

#########################################################################################
## funciones de la api llamadas por ajax
#######################################################################################

@main.route('/api/get/<int:userid>/<date>')
@main.route('/api/get/<int:userid>/<date>/<int:page>')
@main.route('/api/get/<int:userid>/<date>/<int:page>/<int:labelid>')
@login_required
def apiget(userid, date, page=1, labelid=None):
    pagesize = 20
    if labelid is not None:
        pictures = Picture.query.filter(Picture.user_id==userid)\
                .filter(db.func.strftime('%Y-%m-%d', date)==db.func.strftime('%Y-%m-%d', Picture.date))\
                .filter(Picture.label_id==labelid)\
                .paginate(page, pagesize, False).items
    else:
        pictures = Picture.query.filter(Picture.user_id==userid)\
                .filter(db.func.strftime('%Y-%m-%d', date)==db.func.strftime('%Y-%m-%d', Picture.date))\
                .paginate(page, pagesize, False).items
    nextpage = page + 1
    morepages = len(pictures) == pagesize # si hay menos items que el tamaño del paginado es que ya no hay mas paginas
    # basic response structure
    result = {'working': True, 'next-page': nextpage, 'label-id': labelid, 'user-id': userid, 'more-pages': morepages}
    # incluimos la id, el path, el label y el datetime
    pictures = {picture.id: {'path': picture.path, 'label': picture.label_id, 'id': picture.id, 'datetime': picture.date.isoformat()} for picture in pictures}
    result['pictures'] = pictures
    # dumping data
    js = json.dumps(result)
    resp = Response(js, status=200, mimetype='application/json')
    return resp


@main.route('/api/set', methods=['POST'])
@login_required
def api_db_set():
    data = request.get_json()
    #print "the requested data:"
    #print data

    # update all elements by id
    for id in data['keys']:
        picture = Picture.query.filter_by(id=id).first()
        picture.label_id = data['label']
        db.session.add(picture)

    db.session.commit()

    return Response('{"status":true}', status=200, mimetype='application/json')