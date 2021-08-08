from endpoints import TmdbService
from unittest.mock import Mock

tmdb_client = TmdbService()

def test_get_poster_url_uses_default_size():
   # Przygotowanie danych
   poster_api_path = "some-poster-path"
   expected_default_size = 'w342'
   # Wywołanie kodu, który testujemy
   poster_url = tmdb_client.get_poster_url_endpoint(poster_path=poster_api_path)
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
