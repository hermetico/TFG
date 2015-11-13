# -*- coding: utf-8 -*-
DEFAULT_LABELS = [
    'Tareas domesticas',
    'Conduciendo',
    'Cocinando',
    'Deporte',
    'Leyendo',
    'Perros',
    'Gatos',
    'Descansando',
    'Comiendo',
    'trabajando',
    'Charlando',
    'TV',
    'Comprando',
    'Bicicleta',
    'Familia',
    'Reunion',
    'WC',
    'Transporte'
]

def create_admin_role(db, Role):
    role = Role.query.first()
    if role:
        print "Administrator role is already in the database, skipping this step"
        return

    nombre = raw_input("Inserta un nombre para el rol de Administrador (default:Administrador): ") or "Administrador"
    role = Role(name=nombre)
    db.session.add(role)

    nombre = raw_input("Inserta un nombre para el rol de Usuario (default:Usuario): ") or "Usuario"
    role = Role(name=nombre)
    db.session.add(role)

    db.session.commit()


def create_admin_user(db, User):
    user = User.query.first()
    if user:
        print "Administrator user is already in the database, skipping this step"
        return

    nombre = raw_input("Inserta un nombre para el usuario administrador(default:admin): ") or "admin"
    password = raw_input("Inserta una password para el usuario administrador(default:admin): ") or "admin"
    # ojo que es casesensitive, ponemos el nombre en lower
    user = User(username=nombre.lower(), password=password, role_id=1) # default admin role is 1
    db.session.add(user)
    user = User(username="lifelogging", password="LogTeamBCN@15", role_id=1)
    db.session.add(user)
    db.session.commit()


def create_default_label(db, Label):

    label = Label.query.first()
    if label:
        print "Default label is already in the database, skipping this step"
        return
    nombre = raw_input("Inserta un nombre para la etiqueta por defecto(default:sin-etiqueta)") or "sin-etiqueta"
    label = Label(name=nombre)
    db.session.add(label)

    # añadimos las etiquetas extra
    for nombre in DEFAULT_LABELS:
        print "Añadiendo etiquta %s"%(nombre)
        label = Label(name=nombre)
        db.session.add(label)

    db.session.commit()


def initial_deploy(context):
    """Genera los datos necesarios para ejecutar la app inicialmente"""
    print "Generando tablas en la base de datos"
    context['db'].create_all()
    create_admin_role(context['db'], context['Role'])
    create_admin_user(context['db'], context['User'])
    create_default_label(context['db'], context['Label'])
    print "Ya puedes iniciar la aplicacion"


