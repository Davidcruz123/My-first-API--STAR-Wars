from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String,Date




db=SQLAlchemy()            #preguntar

class LogIn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250),nullable=False)
    last_name = db.Column(db.String(250),nullable=False)
    user_name = db.Column(db.String(250), unique=True,nullable=False)
    email = db.Column(db.String(250), unique=True,nullable=False)
    password = db.Column(db.String(100),nullable=False)
    prueba=db.Column(db.String(10))

    def __repr__(self):
        return '<Username %r>' %self.user_name
