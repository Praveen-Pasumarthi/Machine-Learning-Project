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

# Computing the similarity matrix
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

            # Cleans and searches for the movie in the CSV
            movie_name_clean = movie_data['Title'].strip().lower()
            matching_movies = movies_data[movies_data['title'].str.lower().str.strip() == movie_name_clean]

            if matching_movies.empty:
                st.write(f"Movie '{movie_data['Title']}' not found in the local dataset.")
            
            else:
                # If an exact match is found, display recommendations based on similarity
                index_of_the_movie = matching_movies.index[0]

                # Finding sequels or related movies
                sequels = movies_data[movies_data['title'].str.contains(f"{movie_data['Title']} 2|{movie_data['Title']} II|{movie_data['Title']} Returns", case=False, na=False)]

                # Displays sequels/related movies
                if not sequels.empty:
                    st.write(f"**Sequels/Related Movies:**")
                    for i, title in enumerate(sequels['title']):
                        st.write(f"{i + 1}. {title}")

                # Getting similarity scores
                similarity_score = list(enumerate(similarity[index_of_the_movie]))
                sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

                # Displays recommendations
                st.write(f"Movies recommended based on {matching_movies['title'].values[0]}:")

                recommended_movies = []
                sequel_titles = sequels['title'].tolist() if not sequels.empty else []

                for movie in sorted_similar_movies[1:15]:
                    index = movie[0]
                    title = movies_data.loc[index]['title']

                    # Excludes titles already in the sequels list and the original movie name
                    if title not in sequel_titles and title.lower().strip() != movie_name_clean:
                        recommended_movies.append(title)

                # Displays the final list of recommended movies
                for i, title in enumerate(recommended_movies):
                    st.write(f"{i + 1}. {title}")
        else:
            st.write("No movie found on OMDb API. Please try another name.")
    else:
        st.write("Please enter a movie name.")