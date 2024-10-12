import streamlit as st
import requests

# Function to fetch movie data from OMDb API
def fetch_movie_data(movie_name, api_key):
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
    response = requests.get(url)
    return response.json()

# Function to search movies by genre
def search_movies(genre, api_key):
    url = f"http://www.omdbapi.com/?s={genre}&apikey={api_key}"
    response = requests.get(url)
    return response.json()

# Function to fetch detailed movie information by ID
def fetch_detailed_movie_data(movie_id, api_key):
    url = f"http://www.omdbapi.com/?i={movie_id}&apikey={api_key}"
    response = requests.get(url)
    return response.json()

# Streamlit app
st.title('Movie Recommendation System')

# User input
movie_name = st.text_input("Enter your favorite movie:")
api_key = '45dacc56'  # Your OMDb API key

# Language selection
language_options = ['English', 'Hindi', 'Telugu']
selected_language = st.selectbox("Select Language:", language_options)

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
            st.write(f"**Language:** {movie_data['Language']}")

            # Get genres and prepare for recommendations
            genres = movie_data['Genre'].split(', ')
            recommended_movies = set()  # Using a set to avoid duplicates

            # Search for movies based on genre
            for genre in genres:
                genre = genre.strip()  # Clean genre string
                search_results = search_movies(genre, api_key)

                if search_results['Response'] == 'True':
                    for movie in search_results.get('Search', []):
                        # Fetch detailed movie information for language check
                        detailed_movie_data = fetch_detailed_movie_data(movie['imdbID'], api_key)
                        
                        # Check if the movie language matches the selected language
                        if detailed_movie_data['Response'] == 'True' and selected_language in detailed_movie_data['Language']:
                            recommended_movies.add(detailed_movie_data['Title'])

            # Display recommendations
            if recommended_movies:
                st.write("You might also like:")
                for i, title in enumerate(list(recommended_movies)[:10]):  # Limit to 10 recommendations
                    st.write(f"{i + 1}. {title}")
            else:
                st.write("No recommendations found based on the selected genre and language.")
        else:
            st.write("No movie found. Please try another name.")
    else:
        st.write("Please enter a movie name.")
