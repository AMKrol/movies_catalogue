import requests
import random


class tmdb_service():
    def __init__(self):
        self.endpoint_movie = "https://api.themoviedb.org/3/movie/"
        self.endpoint_poster = "http://image.tmdb.org/t/p/"
        self.list_types = ['popular', 'top_rated', 'upcoming', 'now_playing']

    def get_movies_list_endpoint(self, list_name):
        endpoint = f"{self.endpoint_movie}{list_name}"
        with open("api_token.txt", "r") as tokenfile:
            api_token = tokenfile.read()
        headers = {
            "Authorization": f"Bearer {api_token}"
        }
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
        with open("api_token.txt", "r") as tokenfile:
            api_token = tokenfile.read()
        headers = {
            "Authorization": f"Bearer {api_token}"
        }
        response = requests.get(endpoint, headers=headers)
        return response.json()

    def get_single_movie_cast_endpoint(self, movie_id):
        endpoint = f"{self.endpoint_movie}{movie_id}/credits"
        with open("api_token.txt", "r") as tokenfile:
            api_token = tokenfile.read()
        headers = {
            "Authorization": f"Bearer {api_token}"
        }
        response = requests.get(endpoint, headers=headers)
        return response.json()

    def get_cast_endpoint(self, movie_id, how_many):
        data = self.get_single_movie_cast_endpoint(movie_id)
        random_data = data["cast"][:how_many]
        return random_data

    def get_movie_images_endpoint(self, movie_id):
        endpoint = f"{self.get_movies_endpoint}{movie_id}/images"
        with open("api_token.txt", "r") as tokenfile:
            api_token = tokenfile.read()
        headers = {
            "Authorization": f"Bearer {api_token}"
        }
        response = requests.get(endpoint, headers=headers)
        return response.json()

    def get_random_backdrop_endpoint(self, movie_id):
        movie_images = self.get_movie_images(movie_id)
        return random.choice(movie_images['backdrops'])["file_path"]
