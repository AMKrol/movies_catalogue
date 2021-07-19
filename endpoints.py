import requests
import random


class TmdbService():
    def __init__(self):
        self.endpoint_movie = "https://api.themoviedb.org/3/movie/"
        self.endpoint_poster = "http://image.tmdb.org/t/p/"
        self.endpoint_search = "https://api.themoviedb.org/3/search/movie/"
        self.endpoint_get_tv_airing_today = "https://api.themoviedb.org/3/tv/airing_today"
        self.list_types = ['popular', 'top_rated', 'upcoming', 'now_playing']

    def _make_headers():
        with open("api_token.txt", "r") as tokenfile:
            api_token = tokenfile.read()
        return {
            "Authorization": f"Bearer {api_token}"
        }

    def get_movies_list_endpoint(self, list_name):
        endpoint = f"{self.endpoint_movie}{list_name}"
        headers = self._make_headers()
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_movies_endpoint(self, list_name="popular", how_many=12):
        if list_name not in self.list_types:
            list_name = "popular"
        data = self.get_movies_list_endpoint(list_name)
        random_data = data["results"][:how_many]
        random.shuffle(random_data)
        return random_data

    def get_poster_url_endpoint(self, poster_path, size="w342"):
        return f"{self.endpoint_poster}{size}/{poster_path}"

    def get_single_movie_endpoint(self, movie_id):
        endpoint = f"{self.endpoint_movie}{movie_id}"
        headers = self._make_headers()
        response = requests.get(endpoint, headers=headers)
        return response.json()

    def get_single_movie_cast_endpoint(self, movie_id):
        endpoint = f"{self.endpoint_movie}{movie_id}/credits"
        headers = self._make_headers()
        response = requests.get(endpoint, headers=headers)
        return response.json()

    def get_cast_endpoint(self, movie_id, how_many):
        data = self.get_single_movie_cast_endpoint(movie_id)
        random_data = data["cast"][:how_many]
        return random_data

    def get_movie_images_endpoint(self, movie_id):
        endpoint = f"{self.get_movies_endpoint}{movie_id}/images"
        headers = self._make_headers()
        response = requests.get(endpoint, headers=headers)
        return response.json()

    def get_random_backdrop_endpoint(self, movie_id):
        movie_images = self.get_movie_images(movie_id)
        return random.choice(movie_images['backdrops'])["file_path"]

    def get_movie_search_endpoint(self, query):
        endpoint = f"{self.endpoint_search}?query={query}"
        headers = self._make_headers()
        response = requests.get(endpoint, headers=headers)
        return response.json()

    def search_movie(self, query):
        return self.get_movie_search_endpoint(query)["results"]

    def get_airing_today(self):
        endpoint = f"{self.endpoint_get_tv_airing_today}"
        headers = self._make_headers()
        response = requests.get(endpoint, headers=headers)
        return response.json()

    def airing_today(self):
        return self.get_airing_today()["results"]

    def favories_list(self, list):
        output = []
        for movie in list:
            output.append(self.get_single_movie_endpoint(movie))

        return output
