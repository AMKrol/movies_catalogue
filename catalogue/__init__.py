from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = b'asdagsdcfxz%^*&(3dsg'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from catalogue import routes, models

@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "FavMovies": models.FavMovies
    }
