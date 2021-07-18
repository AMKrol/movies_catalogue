from flask import Flask, render_template, request
from flask import redirect, url_for
from endpoints import TmdbService

app = Flask(__name__)

tmdb_client = TmdbService()


@app.route('/')
def homepage():
    list_type = request.args.get('list_type', "popular")
    movies = tmdb_client.get_movies_endpoint(how_many=8, list_name=list_type)
    return render_template("homepage.html",
                           movies=movies,
                           list_type=list_type,
                           list_types=tmdb_client.list_types)


@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url_endpoint(path, size)
    return {"tmdb_image_url": tmdb_image_url}


@app.route("/movie/<movie_id>")
def movie_details(movie_id):
    return render_template("movie_details.html",
                           movie=tmdb_client.get_single_movie_endpoint(
                               movie_id),
                           cast=tmdb_client.get_cast_endpoint(
                               movie_id, how_many=16),
                           backdrop=tmdb_client.get_random_backdrop_endpoint(movie_id))


@app.route("/search")
def search_movie():
    query = request.args.get('q', "")
    if query == "":
        return redirect(url_for("homepage"))
    movie_list = tmdb_client.search_movie(query)
    return render_template("search.html", search_query=query, movies=movie_list)


@app.route("/airing_today")
def airing_today():
    movie_list = tmdb_client.airing_today()
    return render_template("airing.html", movies=movie_list)


if __name__ == '__main__':
    app.run(debug=True)
