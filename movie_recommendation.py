import streamlit as st
import pandas as pd
import requests
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import random

# OMDb API
def fetch_movie_data(movie_name, api_key):
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
    response = requests.get(url)
    return response.json()

# Loading the dataset
@st.cache_data
def load_data():
    return pd.read_csv('movies.csv')
movies_data = load_data()

# Creating a vectorizer for genres
def create_similarity_matrix(data):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(data['genres'].fillna(''))
    return cosine_similarity(tfidf_matrix)

# Computing the similarity matrix
similarity = create_similarity_matrix(movies_data)

# Streamlit app
st.title('Movie Recommendation System')

# User input
movie_name = st.text_input("Enter your favorite movie:")
api_key = '45dacc56'

if st.button('Get Recommendations'):
    if movie_name:
        # Fetching data from OMDb API
        movie_data = fetch_movie_data(movie_name, api_key)
        if movie_data['Response'] == 'True':
            st.write(f"**Title:** {movie_data['Title']}")
            st.write(f"**Year:** {movie_data['Year']}")
            st.write(f"**Genre:** {movie_data['Genre']}")
            st.write(f"**Plot:** {movie_data['Plot']}")
            st.write(f"**Rating:** {movie_data['imdbRating']}")
            # Cleans and searches for the movie in the CSV
            movie_name_clean = movie_data['Title'].strip().lower()
            matching_movies = movies_data[movies_data['title'].str.lower().str.strip() == movie_name_clean]
            # Finding partial matches for similar titles
            partial_matches = movies_data[movies_data['title'].str.contains(movie_name, case=False, na=False)]

            # Checks if exact match is found
            if matching_movies.empty:
                st.write(f"Exact movie '{movie_data['Title']}' not found in the local dataset.")
                if not partial_matches.empty:
                    st.write(f"**Found {len(partial_matches)} movie(s) related to '{movie_data['Title']}':**")
                    for i, title in enumerate(partial_matches['title']):
                        st.write(f"{i + 1}. {title}")

                # Continues with genre recommendations even if no exact match
                movie_genres = movie_data['Genre'].split(', ')
                genre_filter = '|'.join(genre.strip() for genre in movie_genres)
                genre_recommendations = movies_data[movies_data['genres'].str.contains(genre_filter, case=False, na=False)]
                if not genre_recommendations.empty:
                    st.write(f"**Other Recommendations in the same genre(s):**")
                    recommended_movies = set(genre_recommendations['title'])
                    recommended_movies = list(recommended_movies)
                    random.shuffle(recommended_movies)
                    for i, title in enumerate(recommended_movies[:10]):
                        st.write(f"{i + 1}. {title}")

            else:
                # If match is found, displays recommendations
                index_of_the_movie = matching_movies.index[0]
                # Finding sequels or related movies
                sequels = movies_data[movies_data['title'].str.contains(f"{movie_data['Title']} 2|{movie_data['Title']} II|{movie_data['Title']} Returns|{movie_data['Title']} - Part", case=False, na=False)]
                all_related_movies = pd.concat([sequels, partial_matches]).drop_duplicates(subset='title')
                if not all_related_movies.empty:
                    st.write(f"**Sequels/Related Movies:**")
                    for i, title in enumerate(all_related_movies['title']):
                        st.write(f"{i + 1}. {title}")
                # Getting genre recommendations based on the given movie genre
                movie_genres = movie_data['Genre'].split(', ')
                genre_filter = '|'.join(genre.strip() for genre in movie_genres)
                genre_recommendations = movies_data[movies_data['genres'].str.contains(genre_filter, case=False, na=False) & movies_data['title'].str.lower().str.strip().eq(movie_name_clean)]
                # Displays the final list of genre-based recommended movies
                if not genre_recommendations.empty:
                    st.write(f"**Other Recommendations in the same genre(s):**")
                    recommended_movies = set(genre_recommendations['title'])
                    recommended_movies = list(recommended_movies)
                    random.shuffle(recommended_movies)  # Shuffle the recommendations
                    for i, title in enumerate(recommended_movies[:10]):
                        st.write(f"{i + 1}. {title}")
                else:
                    st.write("No genre-based recommendations found.")
        else:
            st.write("No movie found on OMDb API. Please try another name.")
    else:
        st.write("Please enter a movie name.")