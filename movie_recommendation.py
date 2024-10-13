import streamlit as st
import pandas as pd
import requests
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# OMDb API function (only for movie details, not recommendations)
def fetch_movie_data(movie_name, api_key):
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
    response = requests.get(url)
    return response.json()

# Load the movies dataset
@st.cache_data
def load_data():
    return pd.read_csv('movies.csv')

movies_data = load_data()

# Create a TF-IDF vectorizer for the genres in CSV
def create_similarity_matrix(data):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(data['genres'].fillna(''))
    return cosine_similarity(tfidf_matrix)

# Compute the similarity matrix for recommendations
similarity = create_similarity_matrix(movies_data)

# Streamlit app
st.title('Movie Recommendation System')

# User input
movie_name = st.text_input("Enter your favorite movie:")
api_key = '45dacc56'  # Your OMDb API key

if st.button('Get Recommendations'):
    if movie_name:
        # Fetch data from OMDb API (only for movie details)
        movie_data = fetch_movie_data(movie_name, api_key)

        if movie_data['Response'] == 'True':
            # Display movie details from OMDb API
            st.write(f"**Title:** {movie_data['Title']}")
            st.write(f"**Year:** {movie_data['Year']}")
            st.write(f"**Genre:** {movie_data['Genre']}")
            st.write(f"**Plot:** {movie_data['Plot']}")
            st.write(f"**Rating:** {movie_data['imdbRating']}")

            # Search for the movie in the CSV based on the title fetched from OMDb
            matching_movie = movies_data[movies_data['title'].str.contains(movie_data['Title'], case=False, na=False)]

            if not matching_movie.empty:
                # If found in CSV, get the index of the movie
                index_of_the_movie = matching_movie.index[0]

                # Compute similarity scores for recommendations
                similarity_score = list(enumerate(similarity[index_of_the_movie]))
                sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

                # Display recommendations from the CSV
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
