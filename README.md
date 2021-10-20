# Movie catalogue

###### Training project

Aim of this project is to learn the basis of Flask web framework and REST API.

## Try it now

This project is available on Heroku platform under https://movie-catalogue-flask.herokuapp.com

## Features

- App allows to get list films with details according to data from REST API
- Select type ot movie list
- working search bar
- 

## Installation on local machine

After clone repository create virtual repository and install dependences:

```sh
cd movies_catalogue/
python -m venv venv
source venv/bin/activate
pip install -r requrements.txt
```

You must have a API token from [TMDB.org](https://www.themoviedb.org/documentation/api?language=pl). You must create a free account. Next the Api token must be set a environment variable TMDB_API_TOKEN. For Debian based distribution you can run 

```sh
export TMDB_API_TOKEN="your_token"
```

Now the program can be run by following:
```sh
gunicorn main:app
```

Enter to your favorite browser and go to:

```sh 
http://localhost:8000/
```

