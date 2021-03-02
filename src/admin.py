from flask_admin import Admin
from models import db,LogIn
from flask_admin.contrib.sqla import ModelView



def setup_admin(app):
    app.config['SECRET_KEY']='mysecret'
    admin=Admin(app)

    admin.add_view(ModelView(LogIn,db.session))