import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

def load_data():
    # Load the dataset from the CSV file
    movies = pd.read_csv('data/movie.csv')
    return movies

def content_based_recommendation(user_input, movies):
    count_vectorizer = CountVectorizer(stop_words='english')
    count_matrix = count_vectorizer.fit_transform(movies['genres'])

    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    movie_idx = movies.index[movies['title'] == user_input].tolist()[0]
    sim_scores = list(enumerate(cosine_sim[movie_idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]  # Top 5 similar movies

    recommended_movies = [movies['title'].iloc[i[0]] for i in sim_scores]
    return recommended_movies

def get_recommendations(genre, rating):
    movies = load_data()

    # Filter by genre if a specific genre is selected
    if genre != 'all':
        movies = movies[movies['genres'].str.contains(genre, case=False, na=False)]

    # Filter by rating if provided
    if rating:
        movies = movies[movies['rating'] >= float(rating)]

    recommendations = movies['title'].head(5).tolist()
    return recommendations

