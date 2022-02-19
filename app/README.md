# Casting Agency

#### [Link](https://casting-agency-udacity-capston.herokuapp.com/)

## Definition

This is the final project of Udacity FSND

## Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

 ## Roles

There are three Roles in this API

##### Casting Assistant
##### Casting Director
##### Executive Producer

All tokens are in the `setup.sh` file

## Endpoints

## Movies

### `GET /movies`

##### `Assistant User`

- Fetches all the movies from the database
- Request arguments: None
- Returns: A list of movies contain key:value pairs of id and name

#### `Response`

```json5
{
  "success": true,
  "movies": [
    {
      "id": 1,
      "title": "Movie 1"
    },
    {
      "id": 2,
      "title": "Movie 2",
    }
  ]
}
```

### `GET /movies/<int:movie_id>`

##### `Assistant User`

- Fetches a movie by id from the database
- Request arguments: movie_id
- Returns: A movie json containing key:value pairs of id,
name, release_year, genre and duration

#### `Response`

```json5
{
  "success": true,
  "movie": {
        "duration": 123,
        "genre": "Genre 1",
        "id": 1,
        "name": "Movie 1",
        "release_year": 2022
    },
}
```

### `POST /movies`

##### `Director User`

- Creates a movie and pushes it into the database
- Request arguments: None
- Returns: short form of movie added and success state

#### `Body`

```json5
{
    "name": "Movie 1",
    "release_year": 2000,
    "duration":180,
    "genre": "Genre 1"
}
```

#### `Response`

```json5
{
    "success": true,
    "movie": {
        "id": 1,
        "name": "Movie 1"
    }
}
```

### `PATCH /movies/<int:movie_id>`

##### `Director User`

- Updates a movie and pushes it into the database
- Request arguments: movie_id
- Returns: Short form of movie updated and success state

#### `Body`

```json5
{
    "name": "Another Movie"
}
```

#### `Response`

```json5
{
    "success": true,
    "movie": {
        "id": 1,
        "name": "Another Movie"
    }
}
```

### `DELETE /movies/<int:movie_id>`

##### `Producer User`

- Deletes a movie from the database
- Request arguments: movie_id
- Returns: Short form of movie deleted and success state

#### `Response`

```json5
{
    "success": true,
    "movie": {
        "id": 1,
        "name": "Deleted Movie"
    }
}
```

## Actors

### `GET /actors`

##### `Assistant User`

- Fetches all the actors from the database
- Request arguments: None
- Returns: A list of actors contain key:value pairs of id and name

#### `Response`

```json5
{
  "success": true,
  "actors": [
    {
      "id": 1,
      "title": "Actor 1"
    },
    {
      "id": 2,
      "title": "Actor 2",
    }
  ]
}
```

### `GET /actors/<int:actor_id>`

##### `Assistant User`

- Fetches an actor by id from the database
- Request arguments: actor_id
- Returns: An actor json containing key:value pairs of id,
name, gender, and age

#### `Response`

```json5
{
    "success": true,
    "actor": {
        "age": 35,
        "gender": "female",
        "id": 1,
        "name": "Actor 1"
    },
}
```

### `POST /actors`

##### `Director User`

- Creates an actor and pushes it into the database
- Request arguments: None
- Returns: short form of actor added and success state

#### `Body`

```json5
{
    "name": "Actor 1",
    "age": 30,
    "gender": "female"
}
```

#### `Response`

```json5
{
    "success": true,
    "actor": {
        "id": 1,
        "name": "Actor 1"
    },
}
```

### `PATCH /actors/<int:actor_id>`

##### `Director User`

- Updates an actor and pushes it into the database
- Request arguments: actor_id
- Returns: Short form of actor updated and success state

#### `Body`

```json5
{
    "name": "Another Actor"
}
```

#### `Response`

```json5
{
    "success": true,
    "actors": {
        "id": 1,
        "name": "Another Actor"
    }
}
```

### `DELETE /actors/<int:actor_id>`

##### `Producer User`

- Deletes an actor from the database
- Request arguments: actor_id
- Returns: Short form of actor deleted and success state

#### `Response`

```json5
{
    "success": true,
    "actors": {
        "id": 1,
        "name": "Deleted Actor"
    }
}
```
