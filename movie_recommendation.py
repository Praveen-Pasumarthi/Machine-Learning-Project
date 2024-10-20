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
api_key = '45dacc56'

if st.button('Get Recommendations'):
    if movie_name:
        # Fetching data from OMDb API
        movie_data = fetch_movie_data(movie_name, api_key)
        if movie_data['Response'] == 'True':
            st.write(f"**Title:** {movie_data['Title']}")
            st.write(f"**Year:** {movie_data['Year']}")
            st.write(f"**Genre:** {movie_data['Genre']}")
            st.write(f"**Plot:** {movie_data['Plot']}")
            st.write(f"**Rating:** {movie_data['imdbRating']}")
            # Clean and search for the movie in the CSV
            movie_name_clean = movie_data['Title'].strip().lower()
            matching_movies = movies_data[movies_data['title'].str.lower().str.strip() == movie_name_clean]
            # Finding sequels from the OMDb API
            sequels_from_api = []
            if 'Related' in movie_data and movie_data['Related']:
                sequels_from_api = movie_data['Related'].split(", ")
            else:
                sequels_from_api = []  # If the API doesn't provide sequels
            # Finding sequels from CSV file based on the title
            sequels_from_csv = movies_data[movies_data['title'].str.contains(movie_name, case=False, na=False)]['title'].tolist()
            # Check if exact match is found
            if matching_movies.empty:
                st.write(f"Exact movie '{movie_data['Title']}' not found in the local dataset.")
                # Display related movies from partial matches
                partial_matches = movies_data[movies_data['title'].str.contains(movie_name, case=False, na=False)]
                if not partial_matches.empty:
                    st.write(f"**Found {len(partial_matches)} movie(s) related to '{movie_data['Title']}':**")
                    for i, title in enumerate(partial_matches['title']):
                        st.write(f"{i + 1}. {title}")
                # Display sequels found from API and CSV
                combined_sequels = set(sequels_from_api + sequels_from_csv)
                if combined_sequels:
                    st.write(f"**Sequels/Related Movies (from API and CSV):**")
                    for i, title in enumerate(combined_sequels):
                        st.write(f"{i + 1}. {title}")
                else:
                    st.write("No sequels found from the API or CSV.")
                # Collect genre recommendations based on genres from the API
                movie_genres = movie_data['Genre'].split(', ')
                genre_filter = '|'.join(genre.strip() for genre in movie_genres)
                genre_recommendations = set(movies_data[movies_data['genres'].str.contains(genre_filter, case=False, na=False)]['title'])
                
                # Shuffle and display genre recommendations
                if genre_recommendations:
                    st.write(f"**Other Recommendations in the genre(s) ({', '.join(movie_genres)}):**")
                    random_genre_recommendations = list(genre_recommendations)
                    random.shuffle(random_genre_recommendations)
                    for i, title in enumerate(random_genre_recommendations[:10]):
                        st.write(f"{i + 1}. {title}")
                else:
                    st.write("No genre-based recommendations found.")
            else:
                # If an exact match is found, display recommendations based on similarity
                index_of_the_movie = matching_movies.index[0]
                # Displays the sequels found from API and CSV
                combined_sequels = set(sequels_from_api + sequels_from_csv)
                if combined_sequels:
                    st.write(f"**Sequels/Related Movies (from API and CSV):**")
                    for i, title in enumerate(combined_sequels):
                        st.write(f"{i + 1}. {title}")
                else:
                    st.write("No sequels found from the API or CSV.")
                # Getting genre recommendations based on the genre of the input movie
                movie_genres = movie_data['Genre'].split(', ')
                genre_filter = '|'.join(genre.strip() for genre in movie_genres)
                genre_recommendations = set(movies_data[movies_data['genres'].str.contains(genre_filter, case=False, na=False) & movies_data['title'].str.lower().str.strip().eq(movie_name_clean)]['title'])
                # Displays the final list of genre-based recommended movies
                if genre_recommendations:
                    st.write(f"**Other Recommendations in the genre(s) ({', '.join(movie_genres)}):**")
                    random_genre_recommendations = list(genre_recommendations)
                    random.shuffle(random_genre_recommendations)
                    for i, title in enumerate(random_genre_recommendations[:10]):
                        st.write(f"{i + 1}. {title}")
                else:
                    st.write("No genre-based recommendations found.")
        else:
            st.write("No movie found on OMDb API. Please try another name.")
    else:
        st.write("Please enter a movie name.")