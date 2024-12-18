import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie poster from TMDb API using the title
def fetch_poster(movie_title):
    api_key = 'your_tmdb_api_key'  # Replace with your actual TMDb API key
    # Use the movie title to search for the movie
    url = f'https://api.themoviedb.org/3/search/movie?api_key=338f9f0c65e09559b1fb7b7ee89c3650&query={movie_title}&language=en-US'
    response = requests.get(url)
    data = response.json()

    # Check if any movie is found and return the poster path
    if 'results' in data and len(data['results']) > 0:
        poster_path = data['results'][0].get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
    return None  # Return None if no poster is found

# Recommendation function
def recommend(selected_movie_name):
    movie_index = movies[movies['title'] == selected_movie_name].index[0]
    distances = similarity[movie_index]
    recommended_movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in recommended_movies_list:
        movie_title = movies.iloc[i[0]].title  # Use 'title' instead of 'id'

        recommended_movies.append(movie_title)
        # Fetch poster from TMDb API
        recommended_movies_posters.append(fetch_poster(movie_title))

    return recommended_movies, recommended_movies_posters

# Load the movie data and similarity data from pickle files
movies = pickle.load(open('movies.pkl', 'rb'))  # This should be a DataFrame
similarity = pickle.load(open('similarity.pkl', 'rb'))  # This should be a numpy array or matrix

st.title('Movie Recommender System')

# Create a selectbox to choose a movie
selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['title'].values  # Use the 'title' column from the DataFrame
)

# When the recommend button is clicked, show movie recommendations
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    # Display movie names and posters in columns
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        if posters[0]:
            st.image(posters[0])
    with col2:
        st.text(names[1])
        if posters[1]:
            st.image(posters[1])
    with col3:
        st.text(names[2])
        if posters[2]:
            st.image(posters[2])
    with col4:
        st.text(names[3])
        if posters[3]:
            st.image(posters[3])
    with col5:
        st.text(names[4])
        if posters[4]:
            st.image(posters[4])


