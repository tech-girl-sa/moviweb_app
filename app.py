import os

from flask import Flask, render_template, request, redirect, url_for

from datamanager.data_manager import SQLiteDataManager
from datamanager.data_models import User, Movie
from omdb_api import OMDbApi

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'data', 'movies.sqlite')

app = Flask(__name__)
data_manager = SQLiteDataManager(db_path, app)


@app.route('/')
def home():
    return "Welcome to MovieWeb App!"


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>')
def user_movies(user_id):
    message = request.args.get("message")
    movies = data_manager.get_user_movies(user_id)
    user = data_manager.get_user(user_id)
    return render_template('user_movies.html', movies=movies, user=user, message=message)


@app.route('/add_user', methods=["GET","POST"])
def add_user():
    if request.method == "GET":
        return render_template('add_user.html')
    else:
        form = dict(request.form)
        user = User(**form)
        data_manager.add_user(user)
        message=f"Welcome {user.name} this is your movies page. Start adding your favorite movies!"
        return redirect(url_for("user_movies", user_id=user.id, message=message))


@app.route('/users/<user_id>/update_movie/<movie_id>', methods=["GET","POST"])
def edit_movie(user_id, movie_id):
    movie = data_manager.get_movie(movie_id)
    if request.method == "GET":
        return render_template('edit_movie.html', movie=movie)
    else:
        data = dict(request.form)
        data_manager.update_movie(movie_id, data)
        message=f"Movie {movie.name} successfully updated!"
        return redirect(url_for("user_movies", user_id=user_id, message=message))


@app.route('/users/<user_id>/add_movie', methods=["GET","POST"])
def add_movie(user_id):
    if request.method == "GET":
        manual_entry = request.args.get("manual_entry", "").lower() == "true"
        show_modal = request.args.get("show_modal", "").lower() == "true"
        if  show_modal:
            return render_template('add_movie.html', show_modal=True, user_id=user_id,
                                   manual_entry=manual_entry)
        else:
            return render_template('add_movie.html', user_id=user_id, manual_entry=manual_entry)
    else:
        data = dict(request.form)
        if len(data) == 1:
            title= data["name"]
            try:
                movie_data = OMDbApi.get_movie(title)
                movie = Movie(**movie_data)
            except:
                return redirect(url_for("add_movie", user_id=user_id, show_modal=True) )
        else:
            movie = Movie(**data)
        movie.user_id = user_id
        data_manager.add_movie(movie)
        message = f"Movie {movie.name} successfully added!"
        return redirect(url_for("user_movies", user_id=user_id, message=message))

@app.route('/users/<user_id>/delete_movie/<movie_id>', methods=["GET"])
def delete_movie(user_id, movie_id):
    movie = data_manager.get_movie(movie_id)
    movie_name = movie.name
    data_manager.delete_movie(movie_id)
    message=f"Movie {movie_name} successfully deleted!"
    return redirect(url_for("user_movies", user_id=user_id, message=message))


if __name__=="__main__":
    app.run(debug=True)
