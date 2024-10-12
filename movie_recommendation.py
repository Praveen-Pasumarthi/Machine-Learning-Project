import streamlit as st
import requests

# Function to fetch movie data from OMDb API
def fetch_movie_data(movie_name, api_key):
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
    response = requests.get(url)
    return response.json()

# Mock function to suggest similar movies based on genre
def suggest_similar_movies(genre):
    # This is a placeholder. In practice, you might pull this from a dataset.
    similar_movies = {
        "Action": ["Die Hard", "Mad Max: Fury Road", "John Wick"],
        "Comedy": ["Superbad", "The Hangover", "Step Brothers"],
        "Drama": ["The Shawshank Redemption", "Forrest Gump", "The Godfather"],
        "Horror": ["Get Out", "A Quiet Place", "The Conjuring"],
        "Romance": ["The Notebook", "Titanic", "Pride & Prejudice"],
    }
    return similar_movies.get(genre, [])

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

            # Display recommendations
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
