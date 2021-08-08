from endpoints import TmdbService
from unittest.mock import Mock

tmdb_client = TmdbService()


def test_get_poster_url_uses_default_size():
    # Przygotowanie danych
    poster_api_path = "some-poster-path"
    expected_default_size = 'w342'
    # Wywołanie kodu, który testujemy
    poster_url = tmdb_client.get_poster_url_endpoint(
        poster_path=poster_api_path)
    # Porównanie wyników
    assert expected_default_size in poster_url


def test_get_movies_list_type_popular():
    movies_list = tmdb_client.get_movies_endpoint(list_name="popular")
    assert movies_list is not None


def test_get_movies_list(monkeypatch):
    # Lista, którą będzie zwracać przysłonięte "zapytanie do API"
    mock_movies_list = {"results": ['Movie 1', 'Movie 2']}

    requests_mock = Mock()
    # Wynik wywołania zapytania do API
    response = requests_mock.return_value
    # Przysłaniamy wynik wywołania metody .json()
    response.json.return_value = mock_movies_list
    monkeypatch.setattr("endpoints.requests.get", requests_mock)

    movies_list = tmdb_client.get_movies_endpoint(list_name="popular")

    for movie in mock_movies_list["results"]:
        if movie not in movies_list:
            assert False, "movie not in list"


def test_get_single_movie_ansqer():
    movies_list = tmdb_client.get_single_movie_endpoint(436969)
    assert movies_list is not None

def test_get_single_movie_images_ansqer():
    movies_list = tmdb_client.get_movie_images_endpoint(436969)
    assert movies_list is not None 

def test_get_cast_endpoint(monkeypatch):
    mock_movies_list = {"cast": ['Actor 1', 'Actor 2','Actor 3', 'Actor 4','Actor 5', 'Actor 6']}

    requests_mock = Mock()
    response = requests_mock.return_value
    response.json.return_value = mock_movies_list
    monkeypatch.setattr("endpoints.requests.get", requests_mock)

    movies_list = tmdb_client.get_cast_endpoint(movie_id=436969, how_many=3)

    for movie in movies_list:
        if movie not in mock_movies_list["cast"]:
            assert False, "actor not in list"
