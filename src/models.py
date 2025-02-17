from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(20), nullable=True)
    lastname = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "lastname": self.lastname,
            "email": self.email,
        }

class Planet(db.Model):
    __tablename__ = 'planet'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    climate = db.Column(db.String, nullable=False)
    diameter = db.Column(db.String, nullable=False)
    gravity = db.Column(db.String, nullable=False)
    population = db.Column(db.String, nullable=False)
    terrain = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Planet {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "population": self.population,
            "terrain": self.terrain
        }

class People(db.Model):
    __tablename__ = 'people'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    eye_color = db.Column(db.String, nullable=False)
    skin_color = db.Column(db.String, nullable=False)
    hair_color = db.Column(db.String, nullable=False)
    birth_year = db.Column(db.String, nullable=False)
    
    def __repr__(self):
        return f'<People {self.name}>'
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "eye_color": self.eye_color,
            "skin_color": self.skin_color,
            "hair_color": self.hair_color,
            "birth_year": self.birth_year
        }

# TABLAS INTERMEDIAS PARA FAVORITOS

class FavoritePlanet(db.Model):
    __tablename__ = 'favorite_planet'

    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref='favorite_planets')
    planet = db.relationship('Planet', backref='favorited_by')

    def __repr__(self):
        return f'<FavoritePlanet User:{self.user_id} Planet:{self.planet_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "planet": self.planet_id,
            "user": self.user_id
        }

class FavoritePeople(db.Model):
    __tablename__ = 'favorite_people'

    id = db.Column(db.Integer, primary_key=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref='favorite_people')
    people = db.relationship('People', backref='favorited_by')

    def __repr__(self):
        return f'<FavoritePeople User:{self.user_id} People:{self.people_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "people": self.people_id,
            "user": self.user_id
        }
