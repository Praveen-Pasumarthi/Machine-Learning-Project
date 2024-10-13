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

# Print column names for debugging
st.write("Columns in CSV: ", movies_data.columns)  # Check column names in the CSV

# Ensure there's an 'index' column, otherwise use the DataFrame's own index
if 'index' not in movies_data.columns:
    movies_data.reset_index(inplace=True)

# Create a TF-IDF vectorizer for the genres
def create_genre_similarity_matrix(data):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    # Vectorize the 'genres' column, filling any missing values
    tfidf_matrix = tfidf_vectorizer.fit_transform(data['genres'].fillna(''))
    return cosine_similarity(tfidf_matrix)

# Compute the similarity matrix based on genres
genre_similarity = create_genre_similarity_matrix(movies_data)

# Streamlit app
st.title('Movie Recommendation System Based on Genres')

# User input
movie_name = st.text_input("Enter your favorite movie:")
api_key = '45dacc56'  # Your OMDb API key

if st.button('Get Recommendations'):
    if movie_name:
        # Fetch data from OMDb API
        movie_data = fetch_movie_data(movie_name, api_key)

        if movie_data.get('Response') == 'True':
            st.write(f"**Title:** {movie_data['Title']}")
            st.write(f"**Year:** {movie_data['Year']}")
            st.write(f"**Genre:** {movie_data['Genre']}")
            st.write(f"**Plot:** {movie_data['Plot']}")
            st.write(f"**Rating:** {movie_data['imdbRating']}")

            # Normalize movie title for comparison (lowercase, remove spaces)
            normalized_title = movie_data['Title'].strip().lower()
            st.write(f"Normalized Title for Search: {normalized_title}")

            # Check for the movie in the CSV data directly by title (case-insensitive match)
            matching_movie = movies_data[movies_data['title'].str.lower() == normalized_title]

            if not matching_movie.empty:
                index_of_the_movie = matching_movie.index[0]  # Use the row index

                # Get genre-based similarity scores
                similarity_score = list(enumerate(genre_similarity[index_of_the_movie]))
                sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

                # Display recommendations from the CSV
                st.write(f"Movies recommended based on similar genres to '{movie_data['Title']}':")
                for i, movie in enumerate(sorted_similar_movies[1:11]):  # Top 10 recommendations
                    index = movie[0]
                    title = movies_data.iloc[index]['title']  # Access the movie title by row index
                    genres = movies_data.iloc[index]['genres']  # Access the genres
                    st.write(f"{i + 1}. {title} - Genres: {genres}")
            else:
                st.write(f"Movie '{movie_data['Title']}' not found in the local dataset for recommendations.")
        else:
            st.write("No movie found on OMDb API. Please try another name.")
    else:
        st.write("Please enter a movie name.")