import requests
import random


def get_popular_movies():
    endpoint = "https://api.themoviedb.org/3/movie/popular"
    with open("api_token.txt", "r") as tokenfile:
        api_token = tokenfile.read()
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()


def get_movies_list(list_name):
    endpoint = f"https://api.themoviedb.org/3/movie/{list_name}"
    with open("api_token.txt", "r") as tokenfile:
        api_token = tokenfile.read()
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()
    return response.json()


def get_movies(list_name="popular", how_many=12):
    data = get_movies_list(list_name)
    random_data = data["results"][:how_many]
    random.shuffle(random_data)
    return random_data


def get_poster_url(poster_path, size="w342"):
    return "http://image.tmdb.org/t/p/"+size+"/"+poster_path


def get_single_movie(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}"
    with open("api_token.txt", "r") as tokenfile:
        api_token = tokenfile.read()
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()


def get_single_movie_cast(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    with open("api_token.txt", "r") as tokenfile:
        api_token = tokenfile.read()
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()


def get_cast(movie_id, how_many):
    data = get_single_movie_cast(movie_id)
    random_data = data["cast"][:how_many]
    return random_data


def get_movie_images(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}/images"
    with open("api_token.txt", "r") as tokenfile:
        api_token = tokenfile.read()
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()


def get_random_backdrop(movie_id):
    movie_images = get_movie_images(movie_id)
    return random.choice(movie_images['backdrops'])["file_path"]
