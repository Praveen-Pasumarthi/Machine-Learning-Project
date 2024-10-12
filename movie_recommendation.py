import streamlit as st
import pandas as pd
import difflib

# Load the movies dataset
movies_data = pd.read_csv('movies.csv') 

# Streamlit app
st.title('Movie Recommendation System')

# User input
movie_name = st.text_input("Enter your favorite movie:")

if st.button('Get Recommendations'):
    if movie_name:
        # Check for a close match of the movie
        list_of_all_titles = movies_data['title'].tolist()
        find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)
        
        if find_close_match:
            close_match = find_close_match[0]
            index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]

            similarity = ...  # Add your similarity calculation here
            similarity_score = list(enumerate(similarity[index_of_the_movie]))
            sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

            st.write(f"Movies recommended based on {close_match}:")
            for i, movie in enumerate(sorted_similar_movies[1:11]):  # Top 10 recommendations
                index = movie[0]
                title = movies_data[movies_data.index == index]['title'].values[0]
                st.write(f"{i+1}. {title}")
        else:
            st.write("No close match found. Try another movie.")
    else:
        st.write("Please enter a movie name.")
