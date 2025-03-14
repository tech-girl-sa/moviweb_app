import pytest
from app import app
from datamanager.data_models import User, Movie


@pytest.fixture()
def app_with_db():
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"  # In-memory DB for tests
    })

    with app.app_context():
        from datamanager.data_models import db
        db.create_all()  # Set up fresh database for each test

    yield app

    with app.app_context():
        db.drop_all()  # Cleanup after tests


@pytest.fixture()
def client(app_with_db):
    return app.test_client()


@pytest.fixture()
def runner(app_with_db):
    return app.test_cli_runner()


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200

def test_add_user(client):
    response = client.post("/add_user", data={
        "name": "user1"
    }, follow_redirects=True)
    with app.app_context():
        user = User.query.filter_by(name="user1").one()
    assert user is not None
    message = f"Welcome {user.name} this is your movies page. Start adding your favorite movies!"
    assert response.status_code == 200
    assert message.encode() in response.data


def test_add_movie(client):
    client.post("/add_user", data={
        "name": "user1"
    }, follow_redirects=True)
    response = client.post("/users/1/add_movie", data={
        "name": "the room"
    }, follow_redirects=True)
    with app.app_context():
        movie = Movie.query.filter_by(name="The Room").one()
    assert movie is not None
    assert movie.imdb_id is not None
    message = f"Movie {movie.name} successfully added!"
    assert response.status_code == 200
    assert message.encode() in response.data


def test_edit_movie(client):
    client.post("/add_user", data={
        "name": "user1"
    }, follow_redirects=True)
    client.post("/users/1/add_movie", data={
        "name": "the room"
    }, follow_redirects=True)
    response = client.post("/users/1/update_movie/1", data={
        "name": "my custom movie",
        "director": "john doe"
    }, follow_redirects=True)
    with app.app_context():
        movie = Movie.query.filter_by(id=1).one()
    assert movie is not None
    assert movie.director == "john doe"
    assert movie.name == "my custom movie"
    message=f"Movie {movie.name} successfully updated!"
    assert response.status_code == 200
    assert message.encode() in response.data