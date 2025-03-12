import os

from flask import Flask, render_template

from datamanager.data_manager import SQLiteDataManager
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
    movies = data_manager.get_user_movies(user_id)
    user = data_manager.get_user(user_id)
    return render_template('user_movies.html', movies=movies, user=user)

if __name__=="__main__":
    app.run(debug=True)
