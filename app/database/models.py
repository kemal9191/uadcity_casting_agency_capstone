#--------------------------------------#
# Import ------------------------------#
#--------------------------------------#

import os
from flask_sqlalchemy import SQLAlchemy


#--------------------------------------#
# Database Configuration --------------#
#--------------------------------------#
database_uri = "postgresql://postgres@localhost:5432/capstone"

db = SQLAlchemy()

def setup_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

def db_drop_and_create_all():
    '''
    Drops all tables from database and starts it from stratch
    '''
    db.drop_all()
    db.create_all()


#--------------------------------------#
# Models ------------------------------#
#--------------------------------------#

class Actor(db.Model):
    __tablename__ = "actors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"<Actor {self.name} has been created with id of {self.id}"
    
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def short(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def long(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender
        }


class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"<Movie {self.name} has been created with id of {self.id}"
    
    def __init__(self, id, name, release_year, duration, genre):
        self.id = id
        self.name = name
        self.release_year = release_year
        self.duration = duration
        self.genre = genre
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def short(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def long(self):
        return {
            "id": self.id,
            "name": self.name,
            "release_year": self.release_year,
            "duration": self.duration,
            "genre": self.genre
        }
    
