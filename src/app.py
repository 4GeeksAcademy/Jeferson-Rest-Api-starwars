"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, People, FavoritePeople, FavoritePlanet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#--------------------------USER-------------------------

@app.route('/user', methods=['GET'])
def handle_get_users():
    all_users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), all_users))

    return jsonify(all_users), 200

@app.route('/user/<int:id>', methods=['GET'])
def handle_get_user(id):
    user = User.query.get(id)
    user = user.serialize()

    return jsonify(user), 200

@app.route('/user', methods=['POST'])
def handle_add_user():
    body = request.get_json()
    print(body)
    if 'username' not in body:
        return jsonify({'msg': 'error name not empty'}), 400
    
    if 'email' not in body:
        return jsonify({'msg': 'error email not empty'}), 400
    
    if 'password' not in body:
        return jsonify({'msg': 'error password not empty'}), 400
    
    new_user = User()
    new_user.username = body['username']
    new_user.name = body['name']
    new_user.lastname = body['lastname']
    new_user.email = body['email']
    new_user.password = body['password']

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.serialize()), 201

@app.route('/user/<int:id>', methods=['DELETE'])
def handle_remove_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return jsonify({}), 204

#======================= Favoritos con usuario ==========================
@app.route('/user/favorites/<int:id>', methods=['GET'])
def get_user_favorites(id):
    all_user_planet_favorites = FavoritePlanet.query.filter_by(user_id=id)
    all_user_people_favorites = FavoritePeople.query.filter_by(user_id=id)

    
    return jsonify({
        "favorite_planet": [planet.serialize() for planet in all_user_planet_favorites],
        "favorite_people": [people.serialize() for people in all_user_people_favorites]
    }), 200



#===========================Planetas==============================
@app.route('/planets', methods=['GET'])
def handle_get_planets():
    all_planets = Planet.query.all()
    all_planets = list(map(lambda x: x.serialize(), all_planets))

    return jsonify(all_planets), 200

@app.route('/planets/<int:id>', methods=['GET'])
def handle_get_planet(id):
    planet = Planet.query.get(id)
    if planet is None:
        return jsonify({"msg": "Planet not found"}), 404
    planet = planet.serialize()

    return jsonify(planet), 200

@app.route('/planets', methods=['POST'])
def handle_add_planet():
   body = request.get_json()

   new_planet = Planet();
   new_planet.name = body['name']
   new_planet.climate = body['climate']
   new_planet.diameter = body['diameter']
   new_planet.gravity = body['gravity']
   new_planet.population = body['population']
   new_planet.terrain = body['terrain']
   
   db.session.add(new_planet)
   db.session.commit()
   
   return jsonify(new_planet.serialize()), 201

@app.route('/favorite/planet', methods=['POST'])
def add_planet_favorite():
    body = request.get_json()
    if not body:
        return jsonify({"msg": "Request body is missing"}), 400
    
    planet_id = body.get('planet_id')
    user_id = body.get('user_id')

    if not planet_id or not user_id:
        return jsonify({"msg": "planet_id and user_id are required"}), 400

    try:
        favorite = FavoritePlanet(planets_id=planet_id, user_id=user_id)
        db.session.add(favorite)
        planet = Planet.query.get(planet_id)
        planet_serialize = planet.serialize()

        if planet_serialize["stars"] is None:
            planet.stars = 1
        else:
            planet.stars = planet_serialize["stars"]+1

        
        db.session.commit()
        return jsonify(favorite.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 400

@app.route('/planets/<int:id>', methods=['DELETE'])
def handle_remove_planet(id):
    planet = Planet.query.get(id)
    db.session.delete(planet)
    db.session.commit()

    return jsonify({}), 204

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet_favorite(planet_id):
    favorite = FavoritePlanet.query.filter_by(planet_id=planet_id).first()
    if not favorite:
        return jsonify({"msg": "Favorite not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite deleted"}), 200



#=============================People==================================

@app.route('/peoples', methods=['GET'])
def handle_get_peoples():
    all_peoples = People.query.all()
    all_peoples = list(map(lambda x: x.serialize(), all_peoples))

    return jsonify(all_peoples), 200

@app.route('/peoples/<int:id>', methods=['GET'])
def handle_get_people(id):
    people = People.query.get(id)
    if people is None:
        return jsonify({"msg": "People not found"}), 404
    people = people.serialize()

    return jsonify(people), 200

@app.route('/peoples', methods=['POST'])
def handle_add_people():
   body = request.get_json()

   new_people = People();
   new_people.name = body['name']
   new_people.gender = body['gender']
   new_people.eye_color = body['eye_color']
   new_people.skin_color = body['skin_color']
   new_people.hair_color = body['hair_color']
   new_people.birth_year = body['birth_year']
   
   db.session.add(new_people)
   db.session.commit()

@app.route('/peoples/<int:id>', methods=['DELETE'])
def handle_remove_character(id):
    people = People.query.get(id)
    db.session.delete(people)
    db.session.commit()

    return jsonify({}), 204

@app.route('/favorite/people', methods=['POST'])
def add_people_favorite():
    body = request.get_json()
    if not body:
        return jsonify({"msg": "Request body is missing"}), 400
    
    people_id = body.get('people_id')
    user_id = body.get('user_id')

    if not people_id or not user_id:
        return jsonify({"msg": "people_id and user_id are required"}), 400

    try:
        favorite = FavoritePeople(peoples_id=people_id, user_id=user_id)
        db.session.add(favorite)
        people = People.query.get(people_id)
        people_serialize = people.serialize()
        
        if people_serialize["stars"] is None:
            people.stars = 1
        else:
            people.stars = people_serialize["stars"]+1

        db.session.commit()
        return jsonify(favorite.serialize()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 400


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_people_favorite(people_id):
    favorite = FavoritePeople.query.filter_by(people_id=people_id).first()
    if not favorite:
        return jsonify({"msg": "Favorite not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite deleted"}), 200





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


