import streamlit as st
import requests

# Function to fetch movie data from OMDb API
def fetch_movie_data(movie_name, api_key):
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
    response = requests.get(url)
    return response.json()

# Function to fetch movies by genre from OMDb API
def fetch_movies_by_genre(genre, api_key):
    url = f"http://www.omdbapi.com/?s={genre}&apikey={api_key}"
    response = requests.get(url)
    return response.json()

# Streamlit app
st.title('Movie Recommendation System')

# User input
movie_name = st.text_input("Enter your favorite movie:")
api_key = '45dacc56'  # Your OMDb API key

if st.button('Get Recommendations'):
    if movie_name:
        # Fetch movie data from OMDb API
        movie_data = fetch_movie_data(movie_name, api_key)

        if movie_data.get('Response') == 'True':
            # Display movie information
            st.write(f"**Title:** {movie_data['Title']}")
            st.write(f"**Year:** {movie_data['Year']}")
            st.write(f"**Genre:** {movie_data['Genre']}")
            st.write(f"**Plot:** {movie_data['Plot']}")
            st.write(f"**Rating:** {movie_data['imdbRating']}")

            # Fetch similar movies based on the first genre
            genres = movie_data['Genre'].split(', ')
            recommended_movies = []

            for genre in genres:
                genre = genre.strip()  # Clean genre string
                search_results = fetch_movies_by_genre(genre, api_key)

                if search_results.get('Response') == 'True':
                    for movie in search_results.get('Search', []):
                        # Exclude the original movie from recommendations
                        if movie['Title'].lower() != movie_data['Title'].lower():
                            recommended_movies.append(movie['Title'])
                            if len(recommended_movies) >= 10:  # Limit to 10 recommendations
                                break

                if len(recommended_movies) >= 10:  # Stop if we already have 10 recommendations
                    break

            # Display recommendations, ensuring unique movie titles
            recommended_movies = list(set(recommended_movies))[:10]  # Remove duplicates and limit to 10

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
