from flask_admin import Admin

from flask_admin.contrib.sqla import ModelView
from models import db,LogIn,Planets,Characters,Favorites

def setup_admin(app):
    app.config['SECRET_KEY']='mysecret'
    admin=Admin(app)

    admin.add_view(ModelView(LogIn,db.session))
    admin.add_view(ModelView(Favorites,db.session))    
    admin.add_view(ModelView(Planets,db.session))
    admin.add_view(ModelView(Characters,db.session))