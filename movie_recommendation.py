import streamlit as st
import pandas as pd
import requests
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# OMDb API function
def fetch_movie_data(movie_name, api_key):
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
    response = requests.get(url)
    return response.json()

# Load the movies dataset
@st.cache_data
def load_data():
    return pd.read_csv('movies.csv')

movies_data = load_data()

# Function to compute similarity for a specific movie
def compute_similarity_for_movie(data, index):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(data['genres'].fillna(''))

    # Calculate similarity only for the specific movie
    movie_tfidf = tfidf_matrix[index]
    similarity_scores = cosine_similarity(movie_tfidf, tfidf_matrix).flatten()
    return similarity_scores

# Streamlit app
st.title('Movie Recommendation System')

# User input
movie_name = st.text_input("Enter your favorite movie:")
api_key = '45dacc56'  # Your OMDb API key

if st.button('Get Recommendations'):
    if movie_name:
        # Fetch data from OMDb API
        movie_data = fetch_movie_data(movie_name, api_key)

        if movie_data['Response'] == 'True':
            st.write(f"**Title:** {movie_data['Title']}")
            st.write(f"**Year:** {movie_data['Year']}")
            st.write(f"**Genre:** {movie_data['Genre']}")
            st.write(f"**Plot:** {movie_data['Plot']}")
            st.write(f"**Rating:** {movie_data['imdbRating']}")

            # Search for the movie in the CSV data directly by title
            matching_movie = movies_data[movies_data.title.str.lower() == movie_data['Title'].lower()]

            if not matching_movie.empty:
                index_of_the_movie = matching_movie.index[0]

                # Get similarity scores only for this movie
                similarity_scores = compute_similarity_for_movie(movies_data, index_of_the_movie)

                # Get top 10 similar movies
                sorted_similar_movies = sorted(list(enumerate(similarity_scores)), key=lambda x: x[1], reverse=True)

                # Display recommendations
                st.write(f"Movies recommended based on {movie_data['Title']}:")
                for i, movie in enumerate(sorted_similar_movies[1:11]):  # Top 10 recommendations
                    index = movie[0]
                    title = movies_data.loc[index, 'title']
                    st.write(f"{i + 1}. {title}")
            else:
                st.write(f"Movie '{movie_data['Title']}' not found in the local dataset for recommendations.")
        else:
            st.write("No movie found on OMDb API. Please try another name.")
    else:
        st.write("Please enter a movie name.")
