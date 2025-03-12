import os

from flask import Flask

from datamanager.data_manager import SQLiteDataManager


basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'data', 'movies.sqlite')

app = Flask(__name__)
data_manager = SQLiteDataManager(db_path, app)


@app.route('/')
def home():
    return "Welcome to MovieWeb App!"

if __name__=="__main__":
    app.run(debug=True)
