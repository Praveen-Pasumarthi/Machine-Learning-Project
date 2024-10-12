import streamlit as st
import requests
import random

# Function to fetch movie data from OMDb API
def fetch_movie_data(movie_name, api_key):
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
    response = requests.get(url)
    return response.json()

# Extended list of similar movies based on genre
def suggest_similar_movies(genre):
    similar_movies = {
        "Action": ["Die Hard", "Mad Max: Fury Road", "John Wick", "Gladiator", "Inception",
                   "The Dark Knight", "Avengers: Endgame", "Terminator 2: Judgment Day",
                   "The Matrix", "Casino Royale"],
        "Comedy": ["Superbad", "The Hangover", "Step Brothers", "Groundhog Day",
                   "Bridesmaids", "Mean Girls", "Anchorman", "Dumb and Dumber",
                   "21 Jump Street", "The 40-Year-Old Virgin"],
        "Drama": ["The Shawshank Redemption", "Forrest Gump", "The Godfather", "Fight Club",
                  "The Dark Knight", "Pulp Fiction", "Schindler's List", "The Social Network",
                  "Good Will Hunting", "A Beautiful Mind"],
        "Horror": ["Get Out", "A Quiet Place", "The Conjuring", "It", "Hereditary",
                   "The Shining", "Halloween", "Sinister", "Scream", "The Babadook"],
        "Romance": ["The Notebook", "Titanic", "Pride & Prejudice", "La La Land",
                    "500 Days of Summer", "Crazy, Stupid, Love.", "A Walk to Remember",
                    "Notting Hill", "The Fault in Our Stars", "Before Sunrise"],
        # Add more genres and movies as needed
    }
    
    # Return at least 10 random movies or the maximum available
    movies = similar_movies.get(genre, [])
    return random.sample(movies, min(len(movies), 10)) if len(movies) >= 10 else movies

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

            # Get the first genre for recommendations
            genres = movie_data['Genre'].split(', ')
            recommended_movies = []

            if genres:
                genre = genres[0].strip()  # Take the first genre and strip any whitespace
                recommended_movies = suggest_similar_movies(genre)

            # Ensure at least 10 recommendations
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
