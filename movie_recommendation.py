import streamlit as st
import requests

# Function to fetch movie data from OMDb API
def fetch_movie_data(movie_name, api_key):
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
    response = requests.get(url)
    return response.json()

# Mock function to suggest similar movies based on genre and language
def suggest_similar_movies(genre, language):
    # This is a placeholder. In practice, you might pull this from a dataset.
    similar_movies = {
        "Action": {
            "English": ["Die Hard", "Mad Max: Fury Road", "John Wick"],
            "Hindi": ["Dhoom", "Baaghi"],
            "Telugu": ["Magadheera", "Arjun Suravaram"]
        },
        "Comedy": {
            "English": ["Superbad", "The Hangover", "Step Brothers"],
            "Hindi": ["3 Idiots", "Chhichhore"],
            "Telugu": ["Eega", "Dookudu"]
        },
        "Drama": {
            "English": ["The Shawshank Redemption", "Forrest Gump", "The Godfather"],
            "Hindi": ["Gully Boy", "Queen"],
            "Telugu": ["Ninnu Kori", "Arjun Reddy"]
        },
        "Horror": {
            "English": ["Get Out", "A Quiet Place", "The Conjuring"],
            "Hindi": ["Bhool Bhulaiyaa", "Raaz"],
            "Telugu": ["Chandamama Kathalu", "Gruham"]
        },
        "Romance": {
            "English": ["The Notebook", "Titanic", "Pride & Prejudice"],
            "Hindi": ["Kabir Singh", "Pyaar Ka Punchnama"],
            "Telugu": ["Geetha Govindam", "Fidaa"]
        },
    }
    # Return recommendations for the specified genre and language
    return similar_movies.get(genre, {}).get(language, [])

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
            st.write(f"**Language:** {movie_data['Language']}")

            # Get the first genre and language for recommendations
            genres = movie_data['Genre'].split(', ')
            language = movie_data['Language'].split(', ')[0].strip()  # Take the first language

            recommended_movies = []

            for genre in genres:
                genre = genre.strip()  # Clean genre string
                recommended_movies.extend(suggest_similar_movies(genre, language))

            # Display recommendations, ensuring unique movie titles
            recommended_movies = list(set(recommended_movies))  # Remove duplicates

            if recommended_movies:
                st.write("You might also like:")
                for i, title in enumerate(recommended_movies[:10]):  # Limit to 10 recommendations
                    st.write(f"{i + 1}. {title}")
            else:
                st.write("No recommendations found based on the genre and language.")
        else:
            st.write("No movie found. Please try another name.")
    else:
        st.write("Please enter a movie name.")
