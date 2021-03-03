from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String,Date

db=SQLAlchemy() 

class LogIn(db.Model):
    __tablename__ = 'log_In'
    id = Column(Integer, primary_key=True,nullable=False)
    name = Column(String(250),nullable=False)
    last_name = Column(String(250),nullable=False)
    user_name = Column(String(250),unique=True,nullable=False)
    email=Column(String(250),unique=True,nullable=False)
    password=Column(String(100),nullable=False)

    def __repr__(self):
        return '<Username %r>' %self.user_name
    def serialize_users(self):
        return{"id":self.id,
        "name":self.name,
            "last_name":self.last_name,
            "user_name":self.user_name,
            "email":self.email
            # do not serialize the password
        }




class Characters(db.Model):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    description = Column(String(550))
    hair_color = Column(String(30))
    skin_color = Column(String(30))
    eye_color = Column(String(30))
    gender = Column(String(30))
    name = Column(String(30))
    planet_origin = Column(String(30))
    picture_url = Column(String(200))
    height=Column(Integer)
    mass=Column(Integer)
    birth_year=Column(Date)

    def __repr__(self):
        return 'Personaje %r' %self.name                   #esta funcion es predeterminada para que devuelva un string

    def serialize_people(self):
        return{                                           #al usar esos corchetes, le estamos diciendo, ud me va a devolver un diccionario..
            "id":self.id,                                   # esto es para extraer la info de la db
            "description":self.description,
            "hair_color":self.hair_color,
            "skin_color":self.skin_color,
            "eye_color":self.eye_color,
           "gender":self.gender,
           "name":self.name,
           "planet_origin":self.planet_origin,
           "picture_url":self.picture_url,
           "height":self.height,
           "mass":self.mass,
           "birth_year":self.birth_year
        }


class Planets(db.Model):
    __tablename__ = 'planets'
    id = Column(Integer, primary_key=True)
    description = Column(String(550))
    climate = Column(String(30))
    gravity = Column(String(30))
    name = Column(String(30))
    terrain = Column(String(30))
    picture_url = Column(String(200))
    diameter=Column(Integer)
    rotation_period=Column(Integer)
    orbital_period=Column(Integer)
    population=Column(Integer)
    surface_water=Column(Integer)

    def __repr__(self):
        return 'Planeta %r' %self.name 
    def serialize_planets(self):
        return{
            "id":self.id,
            "description":self.description,
            "climate":self.climate,
            "gravity":self.gravity,
            "name":self.name,
           "terrain":self.terrain,
           "picture_url":self.picture_url,
           "diameter":self.diameter,
           "rotation_period":self.rotation_period,
           "orbital_period":self.orbital_period,
           "population":self.population,
           "surface_water":self.surface_water
        }




class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = Column(Integer, primary_key=True)
    data_type = Column(String(250))
    planets_id = Column(Integer, ForeignKey('planets.id'),nullable=True)
    characters_id = Column(Integer, ForeignKey('characters.id'),nullable=True)
    user_id = Column(Integer, ForeignKey('log_In.id'),nullable=False)
 
    planets = db.relationship(Planets, foreign_keys=planets_id)
    characters = db.relationship(Characters, foreign_keys=characters_id)
    user = db.relationship(LogIn, foreign_keys=user_id)

    def __repr__(self):
        return 'Favorite %r' %self.id                   #esta funcion es predeterminada para que devuelva un string

    def serialize_favorites(self):
        return{
            "id":self.id,
            "data_type":self.data_type,
            "planet_id":self.planets_id,
            "characters_id":self.characters_id,
            "user_id":self.user_id
        }