from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app)


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



@app.route('/')
def index():
    return "Hello"


if __name__=="__main__":
    app.run(debug=True)