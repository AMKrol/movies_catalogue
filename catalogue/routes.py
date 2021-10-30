from catalogue.forms import LoginForm
from flask import render_template, request, flash, url_for, redirect, session
from catalogue import app
from catalogue.models import FavMovies, Users, db
import functools
import babel
from catalogue.endpoints import TmdbService
from wtforms import ValidationError

tmdb_client = TmdbService()

FAVORITES = set()


def login_required(view_func):
    @functools.wraps(view_func)
    def check_permissions(*args, **kwargs):
        if session.get('logged_in'):
            return view_func(*args, **kwargs)
        return redirect(url_for('login', next=request.path))
    return check_permissions


@app.template_filter()
def format_datetime(value):
    format = "dd.MM.y"
    return babel.dates.format_datetime(value, format)


@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url_endpoint(path, size)
    return {"tmdb_image_url": tmdb_image_url}


@app.route('/')
def homepage():
    list_type = request.args.get('list_type', "popular")
    movies = tmdb_client.get_movies_endpoint(how_many=8, list_name=list_type)
    return render_template("homepage.html",
                           movies=movies,
                           list_type=list_type,
                           list_types=tmdb_client.list_types,
                           session=session)


@app.route("/movie/<movie_id>")
def movie_details(movie_id):
    movie = tmdb_client.get_single_movie_endpoint(movie_id)
    cast = tmdb_client.get_cast_endpoint(movie_id, how_many=16)
    backdrop = tmdb_client.get_random_backdrop_endpoint(movie_id)
    return render_template("movie_details.html", movie=movie, cast=cast, backdrop=backdrop)


@app.route("/search")
def search_movie():
    query = request.args.get('q')
    if not query:
        return redirect(url_for("homepage"))
    movie_list = tmdb_client.search_movie(query)
    return render_template("search.html", search_query=query, movies=movie_list)


@app.route("/airing_today")
def airing_today():
    movie_list = tmdb_client.airing_today()
    return render_template("airing.html", movies=movie_list)


@app.route("/favorites/add", methods=['POST'])
@login_required
def add_to_favorites():
    data = request.form
    movie_id = data.get('movie_id')
    movie_title = data.get('movie_title')
    if movie_id:
        FAVORITES.add(movie_id)
    flash(f"Film {movie_title} dodany do Ulubionych")

    return redirect(url_for('homepage'))


@app.route("/favorites")
@login_required
def show_favorites():
    movie_list = tmdb_client.favories_list(FAVORITES)
    return render_template("favorites.html", movies=movie_list)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    errors = None
    next_url = request.args.get('next')
    if request.method == 'POST':
        if form.validate_on_submit():
            user = Users.query.filter_by(username=form.username.data).first()
            if user and user.password == form.password.data:
                session['logged_in'] = True
                session['username'] = "testest"
                session.permanent = True  # Use cookie to store session.
                flash('You are now logged in.', 'success')
                return redirect(next_url or url_for('homepage'))
            else:
                errors = ValidationError("Bad username or password")
                flash('Bad username or password', 'danger')
        else:
            errors = ValidationError("Bad username or password")
            flash('Bad username or password', 'danger')

    print(errors)
    return render_template("login_form.html", form=form, errors=errors)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        flash('You are now logged out.', 'success')
    return redirect(url_for('homepage'))
