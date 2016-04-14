# -*- coding: utf-8 -*-
from flask import render_template, session, redirect, url_for, flash, json, Response, request, send_file
from flask.ext.login import login_required
from .decorators import admin_required
from . import main
from .. import db
from ..models import User, Label, Picture, Role
from .forms import NewUserForm, NewLabelForm, CreateDatasetForm, ChoiceObj, EliminarImagenesSinEtiqueta
from flask import current_app as app

PAGESIZE = 75
CACHED_DATA = {
    'labels-count': {'dirty': True},
    'sequences-count': {'dirty': True},
    'num-pictures':0

}


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

    if check_dirty():
        set_dirty()

    import pygal
    # first, we make sure whether the data is cached or not
    if CACHED_DATA['labels-count']['dirty']:
        print "Calculating data"
        CACHED_DATA['labels-count']['dirty'] = False
        data = Label.query.all()
        labeled_data = []
        for label in data:
            labeled_data.append((label.name, label.pictures.count()))

        CACHED_DATA['labels-count']['data'] = labeled_data

    if CACHED_DATA['sequences-count']['dirty']:
        CACHED_DATA['sequences-count']['dirty'] = False
        data = Picture.query.all()
        sequences = [0] * Label.query.count()
        current_sequence = -1
        for pic in data:
            if current_sequence != pic.label_id:
                current_sequence = pic.label_id
                sequences[current_sequence - 1] += 1

        CACHED_DATA['sequences-count']['data'] = sequences


    data = CACHED_DATA['labels-count']['data']
    chart_labels = pygal.Bar()
    chart_labels.x_labels = ["Num Pictures"]
    chart_labels.title = "%s Pictures" % (Picture.query.count())
    for label in data:
            chart_labels.add(label[0], label[1])

    data = CACHED_DATA['sequences-count']['data']
    chart_sequences = pygal.Bar()
    chart_sequences.x_labels = ["Num Sequences"]
    chart_sequences.title = "%s Sequences" % (sum(data))
    for label in Label.query.all():
        chart_sequences.add(label.name, data[label.id - 1])


    return render_template('index.html', chart_labels=chart_labels, chart_sequences=chart_sequences)


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

@main.route('/advanced', methods=['GET', 'POST'])
@login_required
@admin_required
def advanced():
    form = EliminarImagenesSinEtiqueta()
    if form.validate_on_submit():
        import os, subprocess
        clave = form.clave.data
        if clave == 'eliminar':
            #recuperamos la primera label que es la "sin etiqueta"
            label = Label.query.first()

            # eliminamos las imagenes
            pics = label.pictures.all()
            for pic in pics:
                path_pic = os.path.join(app.config['IMPORTED_PICTURES_FOLDER'], pic.path)
                if os.path.isfile(path_pic):
                    os.remove(path_pic)
            #################################################################################################
            # una vez eliminado el conjunto de imagenes, buscamos por carpetas que hayan podido quedar vacias
            # para eliminarlas tmb
            # de destiny eliminamos las carpetas vacias
            command = ["find", app.config['IMPORTED_PICTURES_FOLDER'], "-empty", "-type", "d", "-delete"]
            p = subprocess.Popen(command)
            p.wait()
            #################################################################################################

            label.pictures.delete()
            db.session.commit()
            set_dirty()
            flash('Imagenes eliminadas correctamente', 'success')
        else:
            flash('La palabra de seguridad introducida no es correcta', 'danger')
        return redirect(url_for('.advanced'))
    return render_template('advanced.html', form=form)

@main.route('/dataset', methods=['GET', 'POST'])
@login_required
@admin_required
def create_dataset():

    #labels = Label.query.all()
    #choices = ChoiceObj('Etiquetas', [ u"%i" % label.id for label in labels])
    #form = CreateDatasetForm(obj=choices)
    #form.select_labels.choices = [(label.id, label.name) for label in labels]

    #if request.method == 'POST':
    #    path = form.append_path.data or ""
    #    test = form.test_percent.data
    #    qLabels = [int(q) for w in form.select_labels.data]

    form = CreateDatasetForm()

    if form.validate_on_submit():
        percent_test = form.test_percent.data
        path = form.append_path.data or ""
        import shutil, os
        pictures = Picture.query.all()
        labels = Label.query.all()
        media_folder = app.config['IMPORTED_PICTURES_FOLDER']
        static_folder = app.config['STATIC_FOLDER']
        zip_file = static_folder + '/dataset'

        # remove old files
        for file_name in ["/train.txt", "/test.txt"]:
            file_name = static_folder + file_name
            if os.path.isfile(file_name):
                os.remove(file_name)

        if percent_test > 0:
            import random
            num_images = len(pictures)
            num_test = int(num_images * (percent_test / 100.))
            test_indices = random.sample(xrange(num_images), num_test)
            test_data = [pictures[i] for i in test_indices]
            train_data = [pictures[i] for i in xrange(num_images)if i not in test_indices]

            # creates the txt
            with open(media_folder + "/train.txt", "wb") as fo:
                for picture in train_data:
                    fo.write('%s%s %s\n' % (path, picture.path, picture.label_id))

            with open(media_folder + "/test.txt", "wb") as fo:
                for picture in test_data:
                    fo.write('%s%s %s\n' % (path, picture.path, picture.label_id))

        else:
            # creates the csv
            with open(media_folder + "/train.txt", "wb") as fo:
                for picture in pictures:
                    fo.write('%s%s %s\n' % (path, picture.path, picture.label_id))

        with open(media_folder + "/labels.txt", "wb") as fo:
            for label in labels:
                fo.write('%s %s\n' % (label.id, label.name))

        # creates the zip using shutil
        shutil.make_archive(zip_file, 'zip', media_folder)

        return send_file(zip_file + '.zip', mimetype='application/zip')




    return render_template('dataset.html', form=form)


#################################################
## Rutas de exportacion
#################################################
@main.route('/export/labels.txt', methods=['GET'])
@login_required
@admin_required
def export_labels():
    labels = Label.query.all()
    response = ""
    for label in labels:
        response += '%s %s\n' % (label.id, label.name)
    return Response(response, mimetype='text/txt')


@main.route('/export/train.txt', methods=['GET'])
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
                               data={'label': 'Año', 'rows': rows, 'baseurl': baseurl, 'less-labeled':less_labeled, 'base-label':1},
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
        # when a label is selected we cannot paginate the same way, because as long as we are setting new labels
        # the number of the pages remain the same, so if we paginate by 50 pictures
        # and in the first page we label 15 pictures, when we request the second page, we'll be missing 15 labels
        # because at this step, those 15 missing pictures will fall into the first page

        # we use session[date] to store the last id requested
        # the page will help us to start from the bottom if page 1 is requested
        # This could happen when refreshing the page
        if date not in session or page == 1:
            pictures = Picture.query.filter(Picture.user_id==userid)\
                .filter(db.func.strftime('%Y-%m-%d', date)==db.func.strftime('%Y-%m-%d', Picture.date))\
                .filter(Picture.label_id==labelid).all()
        else:
            from_id = session[date]
            pictures = Picture.query.filter(Picture.user_id==userid)\
                .filter(db.func.strftime('%Y-%m-%d', date)==db.func.strftime('%Y-%m-%d', Picture.date))\
                .filter(Picture.label_id==labelid).filter(Picture.id > from_id).all()

        pictures = pictures[:pagesize]
        # keep track of the last picture id
        session[date] = pictures[-1].id

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
    set_dirty()

    return Response('{"status":true}', status=200, mimetype='application/json')

def check_dirty():
    return CACHED_DATA['num-pictures'] != Picture.query.count()


def set_dirty():
    CACHED_DATA['labels-count']['dirty'] = True
    CACHED_DATA['sequences-count']['dirty'] = True
    CACHED_DATA['num-pictures'] = Picture.query.count()
