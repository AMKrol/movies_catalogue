from catalogue.forms import LoginForm, SignupForm
from flask import render_template, request, flash, url_for, redirect, session
from catalogue import app
from catalogue.models import FavMovies, Users, db
import functools
import babel
from catalogue.endpoints import TmdbService
from wtforms import ValidationError

tmdb_client = TmdbService()


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
    if session['logged_in']:
        db_movies = FavMovies.query.filter_by(username=session['ID']).all()
        movies_id_list = [x.movieID for x in db_movies]
        for m in movies:
            if m['id'] in movies_id_list:
                m['fav'] = True
            else:
                m['fav'] = False

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
        movie = FavMovies.query.filter_by(movieID=movie_id, username=session['ID']).first()
        if not movie:
            favmovie = FavMovies(movieID=movie_id,
                             username=session['ID']
                             )
            db.session.add(favmovie)
            db.session.commit()
            flash(f"Film {movie_title} dodany do Ulubionych")

    return redirect(url_for('homepage'))


@app.route("/favorites")
@login_required
def show_favorites():
    movieslist = FavMovies.query.filter_by(username=session['ID']).all()
    FAVORITES = [x.movieID for x in movieslist]
    movie_list = tmdb_client.favories_list(FAVORITES)
    return render_template("favorites.html", movies=movie_list)

@app.route("/removefav", methods=['POST'])
@login_required
def remove_from_favorites():
    data = request.form
    movie_id = data.get('movie_id')
    movie = FavMovies.query.filter_by(movieID=movie_id, username=session['ID']).first()
    
    db.session.delete(movie)
    db.session.commit()

    return redirect(url_for('show_favorites'))

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
                session['ID'] = user.id
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


@app.route("/register", methods=["GET", "POST"])
def registerUser():
    form = SignupForm()
    errors = None
    next_url = request.args.get('next')
    if request.method == "POST":
        if form.validate_on_submit():
            user = Users.query.filter_by(username=form.username.data).first()
            if user:
                errors = ValidationError("Username already exists")
                flash("User already exists", 'denger')
            else:
                newuser = Users(
                    username=form.username.data,
                    password=form.password.data
                )
                db.session.add(newuser)
                db.session.commit()
                return redirect(next_url or url_for('homepage'))
        else:
            errors = ValidationError("Password not match")
            flash('Password not match', 'danger')
    return render_template("register_form.html", form=form, errors=errors)
