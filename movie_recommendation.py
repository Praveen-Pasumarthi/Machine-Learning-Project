import streamlit as st
import pandas as pd
import requests
import random

# OMDb API function
def fetch_movie_data(movie_name, api_key):
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
    response = requests.get(url)
    return response.json()

# Loading the dataset
@st.cache_data
def load_data():
    return pd.read_csv('movies.csv')

movies_data = load_data()

# Streamlit app
st.title('Movie Recommendation System')

# User input
movie_name = st.text_input("Enter your favorite movie:")
api_key = '65215297'

if st.button('Get Recommendations'):
    if movie_name:
        # Fetching data from OMDb API
        movie_data = fetch_movie_data(movie_name.strip(), api_key)

        if movie_data.get('Response') == 'True':  # Check if response is valid
            st.write(f"**Title:** {movie_data.get('Title', 'N/A')}")
            st.write(f"**Year:** {movie_data.get('Year', 'N/A')}")
            st.write(f"**Genre:** {movie_data.get('Genre', 'N/A')}")
            st.write(f"**Plot:** {movie_data.get('Plot', 'N/A')}")
            st.write(f"**Rating:** {movie_data.get('imdbRating', 'N/A')}")

            # Normalize the movie title for matching
            movie_name_clean = movie_data.get('Title', '').strip().lower()
            matching_movies = movies_data[movies_data['title'].str.lower().str.strip() == movie_name_clean]

            # Handling sequels (OMDb API doesn't provide a direct field)
            sequels_from_api = movie_data.get('Related', '').split(", ") if 'Related' in movie_data else []
            sequels_from_csv = movies_data[movies_data['title'].str.contains(movie_name, case=False, na=False)]['title'].tolist()

            # Combine and remove duplicates
            combined_sequels = sorted(set(sequels_from_api + sequels_from_csv))

            # Display sequels
            if combined_sequels:
                st.write(f"**Sequels/Related Movies:**")
                for i, title in enumerate(combined_sequels):
                    st.write(f"{i + 1}. {title}")
            else:
                st.write("No sequels found.")

            # Genre-based recommendations
            movie_genres = movie_data.get('Genre', '').split(', ')
            if movie_genres and movie_genres[0]:
                genre_filter = '|'.join([genre.strip() for genre in movie_genres])
                genre_recommendations = sorted(set(movies_data[movies_data['genres'].str.contains(genre_filter, case=False, na=False)]['title']))

                if genre_recommendations:
                    st.write(f"**Recommendations in {', '.join(movie_genres)} Genre:**")
                    random.shuffle(genre_recommendations)
                    for i, title in enumerate(genre_recommendations[:10]):
                        st.write(f"{i + 1}. {title}")
                else:
                    st.write("No genre-based recommendations found.")
            else:
                st.write("No genre information available.")
        else:
            st.write("No movie found on OMDb API. Please try another name.")
    else:
        st.write("Please enter a movie name.")