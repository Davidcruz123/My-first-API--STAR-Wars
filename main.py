from flask import Flask,request,jsonify,json,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String,Date,and_,or_
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db,LogIn,Planets,Characters,Favorites
from admin import setup_admin
import requests
import datetime
## Nos permite hacer las encripciones de contraseñas
from werkzeug.security import generate_password_hash, check_password_hash
## Nos permite manejar tokens por authentication (usuarios) 
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
#CORS es un aspecto de seguridad que no deja que se puedan hacer request a un URL de otro URL, entonces CORS hace que tu aplicacion si acepte requests desde otros URL
from flask_cors import CORS


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
# db=SQLAlchemy(app)
db.init_app(app)             #la db fue creada en models, acá no se, la inicializo creo

CORS(app)          # se usa corps, lo que tiene que ver con seguridad


jwt = JWTManager(app)          #se inicializa lo del toquen

@app.route('/')
def index():
    return "Hello"

@app.route('/people',methods=['GET','POST'])               
def get_people():
    if request.method=='GET':
        response_body=Characters.query.all()   
        print(response_body)                           #cada elemento es del tipo [<Personaje 'personaje'>]
        serializado=map(lambda x:x.serialize_people(),response_body)      #Se le aplica serializado a cada elemento.. esto me lo convierte casi en una lista
        print(serializado)
        datosenlista=list(serializado)      #teniamos un objeto tipo map.. ahora lo pasamos a lista 
        print(datosenlista)
        return jsonify(datosenlista),200              #Convierte a Json
    else:
        url="https://www.swapi.tech/api/people"
        r=requests.get(url)
        data=r.json()
        for x in data['results']:
            r2=requests.get(x['url'])
            data2=r2.json()
            
            propiedades=data2['result']['properties']            
            hairColor=propiedades['hair_color']
            if hairColor==None:
                hairColor="N/A"
            skinColor=propiedades['skin_color']
            eyeColor=propiedades['eye_color']
            gender=propiedades['gender']
            name=propiedades['name']
            
            height=int(propiedades['height'])
            mass=int(propiedades['mass'])
            birth=propiedades['birth_year']
            print(hairColor,skinColor,eyeColor,gender,name,height,mass,birth)
            
            new_post=Characters(hair_color=hairColor,skin_color=skinColor,eye_color=eyeColor,gender=gender,name=name,height=height,mass=mass,birth_year=birth,description="",planet_origin="",picture_url="")
            print(new_post)
            db.session.add(new_post)
            db.session.commit()


        return jsonify("Hecho")

@app.route('/people/<int:people_id>',methods=['GET'])
def get_person(people_id):
    
    try:
        person=Characters.query.get(people_id)    ##esto me devuelve el nombre de __rep__
        serializado=person.serialize_people()
        print(serializado)
        return jsonify(serializado),200
    except:
        return '404 resource not found',404

@app.route('/planets',methods=['GET',"POST"])
def get_planets():
    if request.method=='GET':
        planetas=Planets.query.all()
        serializadoenlista=list(map(lambda x:x.serialize_planets(),planetas))
        return jsonify(serializadoenlista),200
    else:
        url="https://www.swapi.tech/api/planets/"
        r=requests.get(url)                            #obtengo la info de la api
        data=r.json()                                  #se convierte a json

        for x in data['results']:
            r2=requests.get(x['url'])
            data2=r2.json()   
     
            propiedades=data2['result']['properties']            
            climate=propiedades['climate']
           
            gravity=propiedades['gravity']
            name=propiedades['name']
            terrain=propiedades['terrain']
            diameter=propiedades['diameter']
            surface=propiedades['surface_water']
            rotation=int(propiedades['rotation_period'])
            orbital=int(propiedades['orbital_period'])
            population=propiedades['population']            
                                                           #se ingresan la info en la db
            new_post=Planets(climate=climate,gravity=gravity,name=name,terrain=terrain,diameter=diameter,rotation_period=rotation,orbital_period=orbital,population=population,surface_water=surface)
            print(new_post)
            db.session.add(new_post)
            db.session.commit()


        return jsonify("Hecho")




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
@jwt_required()
def from_users_method_favorites(user_id):
    if request.method=='GET':
        if LogIn.query.get(user_id)==None:
            return '404, resorce not found',404
        favoritos=Favorites.query.filter_by(user_id=user_id).all()
        favserializadoenlista=list(map(lambda x:x.serialize_favorites(),favoritos))
        serializadoenlista=favserializadoenlista.copy()
        print(favserializadoenlista,"se usa print")
        for index,data in enumerate(favserializadoenlista):
            print(data)
            if data['planet_id']:
                planeta=Planets.query.get(data['planet_id'])
                serializado=planeta.serialize_planets()
                serializado['fav_id']=favserializadoenlista[index]['id']                
                serializadoenlista[index]=serializado
            else:
                person=Characters.query.get(data['characters_id'])    ##esto me devuelve el nombre de __rep__
                serializado=person.serialize_people()
                serializado['fav_id']=favserializadoenlista[index]['id']
                serializadoenlista[index]=serializado

            

        return jsonify(serializadoenlista),200
    else:
        decode_objet=request.get_json()
        print(decode_objet)

        data_type=decode_objet.get('type')
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

        # print(new_post.id)

        return {"msg":"the element was added","fav_id":new_post.id}

@app.route('/favorite/<int:favorite_id>',methods=['DELETE'])
@jwt_required()
def delete_favorite(favorite_id):
    print(favorite_id)
    elemento=Favorites.query.get(favorite_id)
    print(elemento)
    if elemento==None:
        return "Element does not exist" ,404   
    db.session.delete(elemento)
    db.session.commit()
    return jsonify({"msg":"Favorite deleted"}),200

    
@app.route('/register',methods=['POST'])
def add_user():
    name=request.json.get("name",None)          #Me permite escoger un pedaso del request, no todo .. en este caso si no existe name.. devuelve none
    last=request.json.get("last_name",None) 
    user=request.json.get("user_name",None) 
    email=request.json.get("email",None) 
    passw=request.json.get("password",None) 
    if not name:
        return jsonify('Name is missing'),400
    elif not last:
        return jsonify('Lastname is missing'),400      
    elif not passw:
        return jsonify('Password is missing'),400


    #validar que exista user  y que no esté repetido
    if not user:        
        return jsonify('Username is missing'),400
    else:
        query=LogIn.query.filter_by(user_name=user).first()        ##se usa first pq con none me da error.. si no , solo me devolveria la query en sql structure
        if query:
            return jsonify({"status":"failed","msj":"Username alredy exists"}),400
        # validar que exista email y que no este repetido
    if not email:
        return jsonify({"status":"failed","msj":"Email is missing"}),400
    else:
        query2=LogIn.query.filter_by(email=email).first()
        if query2:
            return jsonify({"status":"failed","msj":"Email already exists"}),400

    new_db_data=LogIn()      #otra manera de ingresar info
    new_db_data.name=name
    new_db_data.last_name=last
    new_db_data.user_name=user
    new_db_data.email=email
    #se codifica la contrasena
    hashed_password = generate_password_hash(passw)
    print(passw,hashed_password)
    ##############################
    new_db_data.password=hashed_password
    db.session.add(new_db_data)
    db.session.commit()
    return jsonify({"success": "Thanks. your register was successfully", "status": "success"}), 200

@app.route('/login',methods=['POST'])
def login():
    
    user=request.json.get("user_name",None) 
    email=request.json.get("email",None) 
    passw=request.json.get("password",None) 
    if not user:
        return jsonify('Username is missing'),400
    elif not email:
        return jsonify('Email is missing'),400      
    elif not passw:
        return jsonify('Password is missing'),400

    db_user=LogIn.query.filter_by(user_name=user).first()      #este tipo de dato <Username 'pedrimaxi2'>
    if not db_user:
        return  jsonify({"status":"failed","msj":"Username does not match"}),400
    if db_user.email!=email:
        return jsonify({"status":"failed","msj":"Email does not match"}),400

    if not check_password_hash(db_user.password, passw):
        return jsonify({"status":"failed","msj":"Password is invalid"}),401

    #crear token
    expiration=datetime.timedelta(days=3)           #Se especifica el tiempo que ese token estará activo
    token=create_access_token(identity=db_user.user_name,expires_delta=expiration)    #se especifica a quien se le va a asignar el toque y el tiempo de expiración

    data={
        "status":"success",
        "user":db_user.serialize_users(),
        "token":token,
        "expires":expiration.total_seconds()*1000   #se pasa a segundos y se multiplica por mil, pq se debe entregar en milisegundos al browser
    }

    return jsonify(data),200




setup_admin(app)            #Se llama a admin


if __name__=="__main__":
    app.run(debug=True)