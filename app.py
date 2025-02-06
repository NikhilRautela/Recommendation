from flask import Flask, request, render_template, redirect, url_for, session, flash
import pickle
import requests
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash

# Load movie data
movies = pickle.load(open('model/movie_list.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

# In-memory user storage (for demonstration purposes)
users = {}

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommendation(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies_name = []
    recommended_movies_poster = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies_name.append(movies.iloc[i[0]].title)

    return recommended_movies_name, recommended_movies_poster

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/login')
def login():
    return render_template("LogIn.html")

@app.route('/SignUp')
def SignUp():
    return render_template("SignUp.html")

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    movie_list = movies['title'].values
    status = False
    if request.method == "POST":
        try:
            if request.form:
                movies_name = request.form['movies']
                print(movies_name)
                recommended_movies_name, recommended_movies_poster = recommendation(movies_name)
                print(recommended_movies_name)
                print(recommended_movies_poster)
                status = True

                return render_template("prediction.html", movies_name=recommended_movies_name, poster=recommended_movies_poster, movie_list=movie_list, status=status)

        except Exception as e:
            error = {'error': e}
            return render_template("prediction.html", error=error, movie_list=movie_list, status=status)

    else:
        return render_template("prediction.html", movie_list=movie_list, status=status)

if __name__ == '__main__':
    app.debug = True
    app.run()