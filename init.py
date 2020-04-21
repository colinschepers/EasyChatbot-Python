import os
from sqlalchemy.exc import IntegrityError
from app import create_app, db
from app.models import User


config_name = os.getenv('FLASK_CONFIG', 'development')
app = create_app(config_name)


with app.app_context():

    db.create_all()

    try:
        admin = User(email="admin@mail.com", username="admin", password="admin", is_admin=True)
        db.session.add(admin)
        db.session.commit()
    except IntegrityError as e:
        print('Unable to add admin user, it probably already exists.')
        db.session.rollback()

    try:
        anonymous = User(email="anonymous@mail.com", username="anonymous", password="anonymous")
        db.session.add(anonymous)
        db.session.commit()
    except IntegrityError as e:
        print('Unable to add anonymous user, it probably already exists.')
        db.session.rollback()
