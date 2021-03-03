from flask import Flask,request,jsonify,json,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String,Date,and_,or_
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db,LogIn,Planets,Characters,Favorites
from admin import setup_admin

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
# db=SQLAlchemy(app)
db.init_app(app)             #la db fue creada en models, acá no se, la inicializo creo



@app.route('/')
def index():
    return "Hello"

@app.route('/people',methods=['GET'])               
def get_people():
    if request.method=='GET':
        response_body=Characters.query.all()   
        print(response_body)                           #cada elemento es del tipo [<Personaje 'personaje'>]
        serializado=map(lambda x:x.serialize_people(),response_body)      #Se le aplica serializado a cada elemento.. esto me lo convierte casi en una lista
        print(serializado)
        datosenlista=list(serializado)      #teniamos un objeto tipo map.. ahora lo pasamos a lista 
        print(datosenlista)
        return jsonify(datosenlista),200              #Convierte a Json

@app.route('/people/<int:people_id>',methods=['GET'])
def get_person(people_id):
    
    try:
        person=Characters.query.get(people_id)    ##esto me devuelve el nombre de __rep__
        serializado=person.serialize_people()
        print(serializado)
        return jsonify(serializado),200
    except:
        return 'This person does not exist'

@app.route('/planets',methods=['GET'])
def get_planets():
    planetas=Planets.query.all()
    serializadoenlista=list(map(lambda x:x.serialize_planets(),planetas))
    return jsonify(serializadoenlista),200
@app.route('/planets/<int:planet_id>',methods=['GET'])
def get_planet(planet_id):
    try:
        planeta=Planets.query.get(planet_id)
        serializado=planeta.serialize_planets()
        return jsonify(serializado),200
    except:
        return '404 resource not found'

@app.route('/users',methods=['GET'])
def get_users():
    users=LogIn.query.all()
    serializadoenlista=list(map(lambda x:x.serialize_users(),users))
    return jsonify(serializadoenlista),200

    
@app.route('/users/<int:user_id>/favorites',methods=['GET','POST'])
def from_users_method_favorites(user_id):
    if request.method=='GET':
        if LogIn.query.get(user_id)==None:
            return '404, resorce not found',404
        favoritos=Favorites.query.filter_by(user_id=user_id).all()
        serializadoenlista=list(map(lambda x:x.serialize_favorites(),favoritos))
        return jsonify(serializadoenlista),200
    else:
        decode_objet=request.get_json()
        print(decode_objet)

        data_type=decode_objet.get('tipo')
        planet_id=decode_objet.get('planet_id')
        characters_id=decode_objet.get('character_id')
        # Con esta query digo.. si el user id ya cuenta con el planeta y el personaje no es null o  si el user id ya cuenta con personaje ey el planeta no es null, traigamelo...
        favoritos_existentes=Favorites.query.filter(or_(and_(Favorites.user_id==user_id,Favorites.planets_id==planet_id,Favorites.planets_id!=None),and_(Favorites.user_id==user_id,Favorites.characters_id==characters_id,Favorites.characters_id!=None))).all()
        #si ya el favorito ya fue agregado, no lo agregue
        if len(favoritos_existentes)>0:
            return "This favorite was already added"
            

        # si el elemento buscado no existe, no agregue nada
        if Planets.query.get(planet_id)==None and Characters.query.get(characters_id)==None:
            return "This element does not exist"
        elif LogIn.query.get(user_id)==None:
            return '404 resource not found'
        
        new_post=Favorites(data_type=data_type,planets_id=planet_id,characters_id=characters_id,user_id=user_id)
        
        db.session.add(new_post)
        db.session.commit()
        return redirect('/users/<int:user_id>/favorites')

@app.route('/favorite/<int:favorite_id>',methods=['DELETE'])
def delete_favorite(favorite_id):
    print(favorite_id)
    elemento=Favorites.query.get(favorite_id)
    print(elemento)
    if elemento==None:
        return "Elemento does not exist" ,404   
    db.session.delete(elemento)
    db.session.commit()
    return jsonify({"msg":"Favorite deleted"}),200

    
setup_admin(app)            #Se llama a admin


if __name__=="__main__":
    app.run(debug=True)