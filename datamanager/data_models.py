from typing import List

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from outils import get_country_flag_emoji

db: SQLAlchemy = SQLAlchemy()



class User(db.Model):
    id : Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str]
    movies: Mapped[List["Movie"]] = relationship(back_populates="user")

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"User:{self.name}"


class Movie(db.Model):
    id : Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str]
    director: Mapped[str] = mapped_column(nullable= True)
    year: Mapped[int]
    rating: Mapped[int] = mapped_column(nullable=True)
    poster: Mapped[str] = mapped_column(nullable=True)
    country: Mapped[str] = mapped_column(nullable=True)
    imdb_id: Mapped[str] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped["User"] = relationship(back_populates="movies")

    def __str__(self):
        return f"{self.name} ({self.year})"

    def __repr__(self):
        return f"Film:{self.name} ({self.year})"

    @property
    def star_rating(self):
        empty_star = "☆"
        star = "★"
        int_rating = int(self.rating+0.4)
        return f"{int_rating * star}{(10 - int_rating) * empty_star}"

    @property
    def country_flags(self):
        return get_country_flag_emoji(self.country)

