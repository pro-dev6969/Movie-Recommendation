from flask import Flask,render_template,request
import pickle
import pandas as pd
import requests

app = Flask(__name__)

movi_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movii = pd.DataFrame(movi_dict)
sim = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=3e8b8a45c89df227924c2819cf7d6de5&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/original/"+data['poster_path']

@app.route("/")
def man():
    return render_template("index.html")

@app.route("/predict",methods =['POST'])
def home():
    mov = request.form['movie']
    movie_index = movii[movii['title'] == mov].index[0]
    distance = sim[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    L = []
    poster_list = []
    for i in movie_list:
        movie_id = movii.iloc[i[0]].movie_id
        poster_list.append(fetch_poster(movie_id))
        L.append(movii.iloc[i[0]].title)
    return render_template("index2.html", data=(L , poster_list))


if __name__ == "__main__":
    app.run(debug=True)
