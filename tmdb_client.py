import requests


def get_popular_movies():
    endpoint = "https://api.themoviedb.org/3/movie/popular"
    with open("api_token.txt", "r") as tokenfile:
        api_token = tokenfile.read()
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()


def get_movies(how_many):
    data = get_popular_movies()
    return data["results"][:how_many]


def get_poster_url(poster_path, size="w342"):
    return "http://image.tmdb.org/t/p/"+size+"/"+poster_path
