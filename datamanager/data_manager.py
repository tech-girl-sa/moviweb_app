from abc import ABC, abstractmethod

from datamanager.data_models import db, User, Movie


class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        pass


class SQLiteDataManager(DataManagerInterface):

    def __init__(self, db_file_name, app):
        self.app = app
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_file_name}"
        db.init_app(app)
        self.db = db


    def get_all_users(self):
        return self.db.session.query(User).all()


    def get_user_movies(self, user_id):
        return self.db.session.query(User).filter(User.id == user_id).one().movies


    def add_user(self, user):
        self.db.session.add(user)
        self.db.session.commit()

    def add_movie(self, movie):
        self.db.session.add(movie)
        self.db.session.commit()

    def delete_movie(self, movie_id):
        self.db.session.query(Movie).filter(Movie.id == movie_id).delete()
        self.db.session.commit()
