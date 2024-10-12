import streamlit as st
import requests

# Function to fetch movie data from OMDb API
def fetch_movie_data(movie_name, api_key):
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
    response = requests.get(url)
    return response.json()

def suggest_similar_movies(genre):
    similar_movies = {
        "Action": ["Die Hard", "Mad Max: Fury Road", "John Wick", "The Dark Knight", "Gladiator"],
        "Comedy": ["Superbad", "The Hangover", "Step Brothers", "Anchorman", "Dumb and Dumber"],
        "Drama": ["The Shawshank Redemption", "Forrest Gump", "The Godfather", "A Beautiful Mind", "The Pursuit of Happyness"],
        "Horror": ["Get Out", "A Quiet Place", "The Conjuring", "Hereditary", "The Exorcist"],
        "Romance": ["The Notebook", "Titanic", "Pride & Prejudice", "La La Land", "A Walk to Remember"],
        "Sci-Fi": ["Inception", "The Matrix", "Interstellar", "Blade Runner 2049", "The Terminator"]
    }
    
    return similar_movies.get(genre, [])[:5]

# Streamlit app
st.title('Movie Recommendation System')

# User input
movie_name = st.text_input("Enter your favorite movie:")
api_key = '45dacc56'

if st.button('Get Recommendations'):
    if movie_name:
        movie_data = fetch_movie_data(movie_name, api_key)

        if movie_data['Response'] == 'True':
            st.write(f"**Title:** {movie_data['Title']}")
            st.write(f"**Year:** {movie_data['Year']}")
            st.write(f"**Genre:** {movie_data['Genre']}")
            st.write(f"**Plot:** {movie_data['Plot']}")
            st.write(f"**Rating:** {movie_data['imdbRating']}")

            genres = movie_data['Genre'].split(', ')
            recommended_movies = []

            if genres:
                genre = genres[0].strip()
                recommended_movies = suggest_similar_movies(genre)

            if recommended_movies:
                st.write("You might also like:")
                for i, title in enumerate(recommended_movies):
                    st.write(f"{i + 1}. {title}")
            else:
                st.write("No recommendations found based on the genre.")
        else:
            st.write("No movie found. Please try another name.")
    else:
        st.write("Please enter a movie name.")
