from flask import Flask, render_template, request
import tmdb_client

app = Flask(__name__)


@app.route('/')
def homepage():
    list_type = request.args.get('list_type', "popular")
    movies = tmdb_client.get_movies(how_many=8, list_name=list_type)
    list_types = ['popular', 'top_rated', 'upcoming', 'popular']
    return render_template("homepage.html", movies=movies,
                           list_type=list_type, list_types=list_types)


@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}


@app.route("/movie/<movie_id>")
def movie_details(movie_id):
    details = tmdb_client.get_single_movie(movie_id)
    cast = tmdb_client.get_cast(movie_id, how_many=16)
    backdrop = tmdb_client.get_random_backdrop(movie_id)
    return render_template("movie_details.html", movie=details,
                           cast=cast, backdrop=backdrop)


if __name__ == '__main__':
    app.run(debug=True)
