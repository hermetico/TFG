# -*- coding: utf-8 -*-
from flask import render_template, session, redirect, url_for, flash, json, Response, request, send_file
from flask.ext.login import login_required
from .decorators import admin_required
from . import main
from .. import db
from ..models import User, Label, Picture, Role
from .forms import NewUserForm, NewLabelForm
from flask import current_app as app

PAGESIZE = 50


@main.context_processor
def current_user():
    # recuperamos los usuarios con imagenes
    users_with_pictures = User.query.join(Picture).filter(User.id == Picture.user_id).all()
    return dict(users_with_pictures=users_with_pictures)

@main.route('/')
def index():
    return redirect(url_for('main.main_page'))


@main.route('/main')
@login_required
def main_page():
    import pygal
    data = Label.query.all()
    chart = pygal.Bar()
    chart.x_labels = ["Num Pictures"]
    for label in data:
        chart.add(label.name, label.pictures.count())
    return render_template('index.html', chart=chart)


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
        user = User(username=form.username.data.lower(), password=form.password.data, role_id=form.role.data)
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
        #batch label creation
        labels = form.label.data
        for nlabel in labels.split(";"):
            nlabel = nlabel.strip()
            label = Label.query.filter_by(name=nlabel).first()
            if label is not None:
                flash('La etiqueta %s ya existe' % label.name, 'danger')
            else:
                label = Label(name=nlabel)
                db.session.add(label)
                flash('Etiqueta  %s registrada correctamente' %label.name, 'success')
        db.session.commit()
        return redirect(url_for('.labels'))
    label_list = Label.query.order_by(Label.id).all()
    return render_template('labels.html', form=form, labels=label_list)


@main.route('/export/train.txt', methods=['GET'])
@login_required
@admin_required
def export_labels():
    labels = Label.query.all()
    response = ""
    for label in labels:
        response += '%s %s\n' % (label.id, label.name)
    return Response(response, mimetype='text/txt')


@main.route('/export/labels.txt', methods=['GET'])
@login_required
@admin_required
def export_train():
    pictures = Picture.query.all()
    response = ""
    for picture in pictures:
        response += '%s %s\n' % (picture.path, picture.label_id)
    return Response(response, mimetype='text/txt')



@main.route('/export/dataset.zip', methods=['GET'])
@login_required
@admin_required
def export_dataset():
    import shutil
    pictures = Picture.query.all()
    labels = Label.query.all()
    media_folder = app.config['IMPORTED_PICTURES_FOLDER']
    static_folder = app.config['STATIC_FOLDER']
    zip_file = static_folder + '/dataset'

    # creates the csv
    with open(media_folder + "/train.txt", "wb") as fo:
        for picture in pictures:
            fo.write('%s %s\n' % (picture.path, picture.label_id))

    with open(media_folder + "/labels.txt", "wb") as fo:
        for label in labels:
            fo.write('%s %s\n' % (label.id, label.name))

    # creates the zip using shutil
    shutil.make_archive(zip_file, 'zip', media_folder)

    return send_file(zip_file + '.zip', mimetype='application/zip')


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
                .filter(Picture.user_id == user.id).group_by(label).all()
        rows = [x[0] for x in rows]

        less_labeled = db.session.query(
                db.func.strftime('%Y-%m-%d', Picture.date).label('each_day'),
                db.func.strftime('%Y', Picture.date).label('year'),
                db.func.strftime('%m', Picture.date).label('month'),
                db.func.strftime('%d', Picture.date).label('day'),
                db.func.count().label('no_labeled')
            ) \
            .filter(Picture.label_id == 1, Picture.user_id == user.id)\
            .group_by('each_day')\
            .order_by(db.desc('no_labeled')).limit(20).all()

        baseurl = url_for('.cataloguser', userid=userid)

        if not rows:
            flash('El usuario %s no tiene imagenes asociadas' % user.username, 'info')
            return redirect(url_for('.index'))
        breadcrumb = [{'text': 'catalogo', 'url': '/catalog/%i' % userid}]

        return render_template('catalog.html',
                               data={'label': 'Año', 'rows': rows, 'baseurl': baseurl, 'less-labeled':less_labeled },
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
    pagesize = PAGESIZE
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
