import streamlit as st
import pandas as pd
import requests
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

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

# Creating a vectorizer for the genres
def create_similarity_matrix(data):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(data['genres'].fillna(''))
    return cosine_similarity(tfidf_matrix)

# Computing similarity matrix
similarity = create_similarity_matrix(movies_data)

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

            # Cleaning and searching for the movie in the CSV
            movie_name_clean = movie_data['Title'].strip().lower()
            matching_movies = movies_data[movies_data['title'].str.lower().str.strip() == movie_name_clean]

            if matching_movies.empty:
                st.write(f"Movie '{movie_data['Title']}' not found in the local dataset.")
                genres = movie_data['Genre'].split(', ')
                genre_matches = movies_data[movies_data['genres'].fillna('').apply(lambda x: any(genre.strip() in x for genre in genres))]

                if not genre_matches.empty:
                    st.write(f"Showing recommendations for genre: {', '.join(genres)}")
                    shuffled_genre_matches = genre_matches.sample(frac=1).head(10)
                    for i, title in enumerate(shuffled_genre_matches['title']):
                        st.write(f"{i + 1}. {title}")
                else:
                    st.write(f"No recommendations found for genres: {', '.join(genres)}.")
            else:
                # If an exact match is found, displays recommendations based on similarity
                index_of_the_movie = matching_movies.index[0]

                sequels = movies_data[movies_data['title'].str.contains(f"{movie_data['Title']} 2|{movie_data['Title']} II|{movie_data['Title']} Returns", case=False, na=False)]

                if not sequels.empty:
                    st.write(f"**Sequels/Related Movies:**")
                    for i, title in enumerate(sequels['title']):
                        st.write(f"{i + 1}. {title}")

                # Getting similarity scores
                similarity_score = list(enumerate(similarity[index_of_the_movie]))
                sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

                st.write(f"Movies recommended based on {matching_movies['title'].values[0]}:")

                # Displaying recommended movies
                recommended_movies = []
                for movie in sorted_similar_movies[1:10]: 
                    index = movie[0]
                    title = movies_data.loc[index]['title']
                    recommended_movies.append(title)

                # Combined sequels and genre-based recommendations
                recommendations = sequels['title'].tolist() + recommended_movies
                recommendations = list(dict.fromkeys(recommendations)) 

                for i, title in enumerate(recommendations):
                    st.write(f"{i + 1}. {title}")
        else:
            st.write("No movie found on OMDb API. Please try another name.")
    else:
        st.write("Please enter a movie name.")