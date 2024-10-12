import streamlit as st
import requests

# Function to fetch movie data from OMDb API
def fetch_movie_data(movie_name, api_key):
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
    response = requests.get(url)
    return response.json()

# Function to search for movies by genre
def search_movies_by_genre(genre, api_key):
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
        # Fetch data from OMDb API
        movie_data = fetch_movie_data(movie_name, api_key)

        if movie_data['Response'] == 'True':
            st.write(f"**Title:** {movie_data['Title']}")
            st.write(f"**Year:** {movie_data['Year']}")
            st.write(f"**Genre:** {movie_data['Genre']}")
            st.write(f"**Plot:** {movie_data['Plot']}")
            st.write(f"**Rating:** {movie_data['imdbRating']}")

            # Get genres for recommendations
            genres = movie_data['Genre'].split(', ')
            recommended_movies = []
            
            # Use each genre to find similar movies
            for genre in genres:
                genre = genre.strip()  # Clean genre string
                search_results = search_movies_by_genre(genre, api_key)

                if search_results['Response'] == 'True':
                    for movie in search_results.get('Search', []):
                        # Check if the title is not the same as the input movie
                        if movie['Title'].lower() != movie_data['Title'].lower():
                            recommended_movies.append(movie['Title'])

                        # Stop if we have 10 recommendations
                        if len(recommended_movies) >= 10:
                            break

                # Stop if we have 10 recommendations
                if len(recommended_movies) >= 10:
                    break

            # Display recommendations, ensuring unique movie titles
            recommended_movies = list(set(recommended_movies))  # Remove duplicates
            recommended_movies = recommended_movies[:10]  # Limit to 10 recommendations

            if recommended_movies:
                st.write("You might also like:")
                for i, title in enumerate(recommended_movies):  # Display the titles
                    st.write(f"{i + 1}. {title}")
            else:
                st.write("No recommendations found based on the genre.")
        else:
            st.write("No movie found. Please try another name.")
    else:
        st.write("Please enter a movie name.")
