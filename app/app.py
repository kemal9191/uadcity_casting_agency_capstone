#--------------------------------------#
# Import ------------------------------#
#--------------------------------------#

import os
import json
from re import A
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from database.models import Actor, Movie, setup_db
from auth.auth import AuthError, requires_auth
#--------------------------------------#
# Configuration -----------------------#
#--------------------------------------#

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # CORS
    CORS(app, resources={r"/*":{"origins": "*"}})

    #CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers",
            "Content-Type, Authorication"
        )
        response.headers.add(
            "Access-Control-Allow-Methods",
            "GET, POST, PATCH, DELETE, OPTIONS"
        )
        
        return response

    #--------------------------------------#
    # Routes ------------------------------#
    #--------------------------------------#
    @app.route('/')
    def health():
        return jsonify({'health': 'Running!!'}), 200


    @app.route('/actors', methods=['GET'])
    @requires_auth("get:actors")
    def get_actors(payload):
        actors_raw = Actor.query.all()

        return jsonify({
            "success": True,
            "actors": [actor.short() for actor in actors_raw]
        }), 200

    
    @app.route('/actors/<int:actor_id>', methods=['GET'])
    @requires_auth('get:actors-detail')
    def get_actor(payload, actor_id):
        actor = Actor.query.get_or_404(actor_id)

        return jsonify({
            "success": True,
            "actor": actor.long()
        }), 200


    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actor')
    def post_actor(payload):
        try:
            request_data = request.get_json()
            if 'name' not in request_data \
                or 'age' not in request_data \
                or 'gender' not in request_data:
                abort(422)
            actor = Actor(name=request_data['name'], age=request_data['age'], gender=request_data['gender'])
            actor.insert() 

            return jsonify ({
                "success": True,
                "actor": actor.short()
            }), 200
        
        except Exception:
            print(str(Exception))
            abort(422)


    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def update_actor(payload, actor_id):
        actor = Actor.query.get_or_404(actor_id)

        try:
            request_data = request.get_json()
            if 'name' in request_data and request_data['name']:
                actor.name = request_data['name']
            if 'age' in request_data and request_data['age']:
                actor.age = request_data['age']
            if 'gender' in request_data and request_data['gender']:
                actor.gender = request_data['gender']
            
            actor.update()
            
            return jsonify({
                "success": True,
                "actor": actor.short()
            }), 200

        except Exception:
            print(str(Exception))
            abort(422)

    
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(payload, actor_id):
        actor = Actor.query.get_or_404(actor_id)

        try:
            actor.delete()
            
            return jsonify({
                "success": True,
                "deleted_actor": actor.short()
            }), 200

        except Exception:
            print(str(Exception))
            abort(500)


    @app.route('/movies', methods=['GET'])
    @requires_auth("get:movies")
    def get_movies(payload):
        movies_raw = Movie.query.all()

        return jsonify({
            "success": True,
            "movies": [movie.short() for movie in movies_raw]
        }), 200

    
    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth('get:movies-detail')
    def get_movie(payload, movie_id):
        movie = Movie.query.get_or_404(movie_id)

        return jsonify({
            "success": True,
            "movie": movie.long()
        }), 200


    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movie')
    def post_movie(payload):
        try:
            request_data = request.get_json()
            if 'name' not in request_data \
                or 'release_year' not in request_data \
                or 'duration' not in request_data \
                or 'genre' not in request_data:
                abort(422)
            movie = Movie(name=request_data['name'], \
                release_year=request_data['release_year'], \
                duration=request_data['duration'], \
                genre=request_data['genre'])
            movie.insert() 

            return jsonify ({
                "success": True,
                "movie": movie.short()
            }), 200
        
        except Exception:
            print(str(Exception))
            abort(422)


    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def update_movie(payload, movie_id):
        movie = Movie.query.get_or_404(movie_id)

        try:
            request_data = request.get_json()
            if 'name' in request_data and request_data['name']:
                movie.name = request_data['name']
            if 'release_year' in request_data and request_data['release_year']:
                movie.release_year = request_data['release_year']
            if 'duration' in request_data and request_data['duration']:
                movie.duration = request_data['duration']
            if 'genre' in request_data and request_data['genre']:
                movie.genre = request_data['genre']
            
            movie.update()
            
            return jsonify({
                "success": True,
                "movie": movie.short()
            }), 200

        except Exception:
            print(str(Exception))
            abort(422)

    
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(payload, movie_id):
        movie = Movie.query.get_or_404(movie_id)

        try:
            movie.delete()
            
            return jsonify({
                "success": True,
                "deleted_movie": movie.short()
            }), 200
            
        except Exception:
            print(str(Exception))
            abort(500)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400


    @app.errorhandler(401)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized"
        }), 401


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not Found"
        }), 404


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422


    @app.errorhandler(405)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
        }), 405


    @app.errorhandler(500)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500


    return app



app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)