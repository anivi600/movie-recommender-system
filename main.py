import pandas as pd
import streamlit as st
st.set_page_config(page_title="Movie Recommender", layout="wide")
import pickle
import requests

movies_dict=pickle.load(open("movie_dict.pkl","rb"))
movies=pd.DataFrame(movies_dict)

def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=31e777399502f5d506ed3a0078359fec"
    response = requests.get(url)
    data = response.json()

    if data.get('poster_path'):
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Poster"

st.title('Movie Recommender System')
select_movie_name=st.selectbox(
    'select movie',
    (movies['title'].values)
)


def recommend(movie):

    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].id
        #fetch poster from API

        print(movies.iloc[i[0]].title)
    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        title = movies.iloc[i[0]].title
        recommended_movies.append(title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters



similarity=pickle.load(open("similarity.pkl","rb"))
if st.button('Recommend'):
    names, posters = recommend(select_movie_name)

    # Row 1
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])

    # Row 2
    cols = st.columns(5)
    for i in range(5,10):
        with cols[i-5]:
            st.text(names[i])
            st.image(posters[i])