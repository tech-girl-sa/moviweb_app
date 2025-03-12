import os

from flask import Flask, render_template, request, redirect, url_for

from datamanager.data_manager import SQLiteDataManager
from datamanager.data_models import User

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

if __name__=="__main__":
    app.run(debug=True)
