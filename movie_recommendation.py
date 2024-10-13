import streamlit as st
import pandas as pd
import difflib
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the movies dataset
@st.cache_data
def load_data():
    return pd.read_csv('movies.csv')

movies_data = load_data()

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

if st.button('Get Recommendations'):
    if movie_name:
        # Case-insensitive and trimmed search for the movie in the CSV data
        movie_name_clean = movie_name.strip().lower()
        matching_movies = movies_data[movies_data['title'].str.lower().str.strip() == movie_name_clean]

        # If exact match fails, try a close match using difflib
        if matching_movies.empty:
            st.write(f"Movie '{movie_name}' not found in the local dataset. Trying similar names...")
            list_of_all_titles = movies_data['title'].str.lower().str.strip().tolist()
            close_matches = difflib.get_close_matches(movie_name_clean, list_of_all_titles, n=3, cutoff=0.6)

            if close_matches:
                st.write(f"Did you mean one of these?")
                for i, match in enumerate(close_matches, 1):
                    st.write(f"{i}. {match.title()}")
                    # Fetch and recommend movies for the first close match found
                closest_match = close_matches[0]
                matching_movies = movies_data[movies_data['title'].str.lower().str.strip() == closest_match]
            else:
                st.write(f"No similar movie names found for '{movie_name}'. Please try again.")

        # If a match (exact or close) is found, display recommendations
        if not matching_movies.empty:
            index_of_the_movie = matching_movies['index'].values[0]

            # Get similarity scores
            similarity_score = list(enumerate(similarity[index_of_the_movie]))
            sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

            # Display recommendations from the CSV
            st.write(f"Movies recommended based on {matching_movies['title'].values[0]}:")
            for i, movie in enumerate(sorted_similar_movies[1:11]):  # Top 10 recommendations
                index = movie[0]
                title = movies_data[movies_data.index == index]['title'].values[0]
                st.write(f"{i + 1}. {title}")
        else:
            st.write(f"No suitable match found for '{movie_name}'. Please try another name.")
    else:
        st.write("Please enter a movie name.")
