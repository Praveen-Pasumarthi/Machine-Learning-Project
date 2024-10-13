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

# Load the movies dataset without caching
def load_data():
    try:
        data = pd.read_csv('movies.csv')
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

movies_data = load_data()

# Ensure movies_data is loaded before proceeding
if movies_data is not None:
    # Create a TF-IDF vectorizer for the genres
    def create_similarity_matrix(data):
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf_vectorizer.fit_transform(data['genres'].fillna(''))
        return cosine_similarity(tfidf_matrix)

    # Compute the similarity matrix
    similarity = create_similarity_matrix(movies_data)

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

                # Normalize movie title for comparison
                normalized_title = movie_data['Title'].strip().lower()  # Normalize title
                st.write(f"Normalized Title for Search: {normalized_title}")

                # Check for the movie in the CSV data directly by title
                if normalized_title in movies_data['title'].str.lower().values:
                    index_of_the_movie = movies_data[movies_data['title'].str.lower() == normalized_title]['index'].values[0]

                    # Get similarity scores
                    similarity_score = list(enumerate(similarity[index_of_the_movie]))
                    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

                    # Display recommendations from the CSV
                    st.write(f"Movies recommended based on {movie_data['Title']}:")
                    for i, movie in enumerate(sorted_similar_movies[1:11]):  # Top 10 recommendations
                        index = movie[0]
                        title = movies_data[movies_data.index == index]['title'].values[0]
                        st.write(f"{i + 1}. {title}")
                else:
                    st.write(f"Movie '{movie_data['Title']}' not found in the local dataset for recommendations.")
            else:
                st.write("No movie found on OMDb API. Please try another name.")
        else:
            st.write("Please enter a movie name.")
else:
    st.write("Movies data could not be loaded.")
