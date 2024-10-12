import streamlit as st
import requests
import random

# Function to fetch movie data from OMDb API
def fetch_movie_data(movie_name, api_key):
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
    response = requests.get(url)
    return response.json()

# Extended list of similar movies based on genre and language
def suggest_similar_movies(genre, language):
    similar_movies = {
        "Action": ["Die Hard", "Mad Max: Fury Road", "John Wick", "Gladiator", "Inception",
                   "The Dark Knight", "Avengers: Endgame", "Terminator 2: Judgment Day",
                   "The Matrix", "Casino Royale", "Black Panther", "Guardians of the Galaxy"],
        "Adventure": ["Jurassic Park", "The Lord of the Rings: The Fellowship of the Ring",
                      "Pirates of the Caribbean: The Curse of the Black Pearl", "Indiana Jones: Raiders of the Lost Ark"],
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

    language_based_movies = {
        "English": ["The Social Network", "La La Land", "Inception", "The Shawshank Redemption", "The Dark Knight"],
        "Spanish": ["Pan's Labyrinth", "Roma", "The Secret in Their Eyes", "Volver", "Amores Perros"],
        "French": ["Amélie", "La Haine", "The Intouchables", "Blue Is the Warmest Color", "Les Misérables"],
        "Hindi": ["3 Idiots", "Dangal", "Kabir Singh", "Gully Boy", "Bajrangi Bhaijaan"],
        "Mandarin": ["Crouching Tiger, Hidden Dragon", "Hero", "The Wandering Earth", "Farewell My Concubine"],
        # Add more languages and movies as needed
    }

    # Collect movies based on genre and language
    recommendations = set()
    
    # Get genre-based recommendations
    if genre in similar_movies:
        recommendations.update(random.sample(similar_movies[genre], min(10, len(similar_movies[genre]))))
    
    # Get language-based recommendations
    if language in language_based_movies:
        recommendations.update(random.sample(language_based_movies[language], min(10, len(language_based_movies[language]))))

    return list(recommendations)

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
            st.write(f"**Language:** {movie_data['Language']}")
            st.write(f"**Plot:** {movie_data['Plot']}")
            st.write(f"**Rating:** {movie_data['imdbRating']}")

            # Get genres and language to recommend based on both
            genres = movie_data['Genre'].split(', ')
            language = movie_data['Language'].split(', ')[0]  # Get the primary language

            recommended_movies = []

            # Collect recommendations from all genres and the language
            for genre in genres:
                recommended_movies.extend(suggest_similar_movies(genre.strip(), language.strip()))

            # Ensure at least 10 unique recommendations
            recommended_movies = list(set(recommended_movies))  # Remove duplicates
            if len(recommended_movies) < 10:
                # If there are not enough unique recommendations, add more random ones
                all_movies = [movie for sublist in similar_movies.values() for movie in sublist]
                recommended_movies += random.sample(all_movies, min(10 - len(recommended_movies), len(all_movies)))
                
            recommended_movies = random.sample(recommended_movies, min(len(recommended_movies), 10))  # Shuffle the final list

            # Display recommendations
            if recommended_movies:
                st.write("You might also like:")
                for i, title in enumerate(recommended_movies):
                    st.write(f"{i + 1}. {title}")
            else:
                st.write("No recommendations found based on the genre and language.")
        else:
            st.write("No movie found. Please try another name.")
    else:
        st.write("Please enter a movie name.")
