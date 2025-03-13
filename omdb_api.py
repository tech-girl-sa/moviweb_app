import os
from dotenv import load_dotenv
from urllib import parse
import requests

load_dotenv()


class OMDbApiException(Exception):
    pass


class OMDbApi:
    API_KEY = os.getenv("OMDbAPI_KEY")
    API_URL = "http://www.omdbapi.com/?"

    @classmethod
    def get_movie(cls, title):
        parameters = {
            "t": title,
            "apikey": cls.API_KEY
        }
        encoded_parameters = parse.urlencode(parameters)
        try:
            response = requests.get(cls.API_URL+encoded_parameters).json()
            if "Error" in response:
                raise OMDbApiException(response["Error"])
            elif "Title" in response:
                title =  response["Title"]
                rating = cls.get_rating_from_response(response)
                year = response.get("Year", None)
                poster = response.get("Poster", "")
                imdb_id = response.get("imdbID", "")
                country = response.get("Country", "")
                director = response.get("Director", "")
                return {
                    "name": title,
                    "rating": rating,
                    "year": year,
                    "poster":poster,
                    "imdb_id": imdb_id,
                    "country": country,
                    "director": director
                }
            else:
               raise  OMDbApiException("There was an issue fetching data from Api")
        except OMDbApiException as e:
            raise e

    @classmethod
    def get_rating_from_response(cls, response):
        if "imdbRating" in response:
            return response["imdbRating"]
        elif "Ratings" in response and len(response["Ratings"])>0:
            return response["Ratings"][0].get("Value", None)

