import streamlit as st
import requests

# Function to fetch movie data from OMDb API
def fetch_movie_data(movie_name, api_key):
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
    response = requests.get(url)
    return response.json()

# Streamlit app
st.title('Movie Recommendation System')

# User input
movie_name = st.text_input("Enter your favorite movie:")
api_key = '45dacc56'

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

            # Basic recommendation logic (this part may need improvement)
            genres = movie_data['Genre'].split(', ')
            recommended_movies = []

            # Fetch movies from OMDb based on the first genre (if available)
            if genres:
                genre = genres[0].strip()  # Take the first genre and strip any whitespace
                genre_movies_data = fetch_movie_data(genre, api_key)  # This may need to be adjusted

                if genre_movies_data['Response'] == 'True':
                    recommended_movies.append(genre_movies_data['Title'])

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
