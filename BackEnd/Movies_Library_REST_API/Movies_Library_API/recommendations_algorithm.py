import numpy as np
from CustomAuthentication.models import User
from Movies_Library_API.models.movie_lib_models import Movie_User, Movie
from sklearn.metrics.pairwise import cosine_similarity


def collaborative_filtering_recommendation_for_movie(user_id, top_n=10):
    user_movies = Movie_User.objects.filter(user=user_id)

    all_users = User.objects.all()
    all_movies = Movie.objects.all()

    ratings_matrix = np.zeros((len(all_users), len(all_movies)))

    user_index_mapping = {}

    for idx, user in enumerate(all_users):
        user_index_mapping[user.id] = idx

    for movie in all_movies:
        ratings = Movie_User.objects.filter(movie=movie.id) \
            .exclude(rating=None) \
            .exclude(rating=0)

        for rating in ratings:
            user_idx = user_index_mapping[rating.user.id]
            movie_idx = rating.id - 1
            ratings_matrix[user_idx, movie_idx] = rating.rating

    user_similarities = cosine_similarity(ratings_matrix)

    user_idx = user_index_mapping[int(user_id)]
    similar_users = np.argsort(user_similarities[user_idx])[::-1][1:]
    recommended_movies = []

    for similar_user_index in similar_users:
        similar_user_id = all_users[int(similar_user_index)].id
        similar_user_movies = Movie_User.objects \
            .filter(user=similar_user_id, status="Watched") \
            .exclude(movie__in=user_movies.values_list("movie_id", flat=True))
        recommended_movies.extend(similar_user_movies)

        if len(recommended_movies) >= top_n:
            break
    return recommended_movies[:top_n]


def collaborative_filtering_recommendation_for_tv_shows():
    ...
