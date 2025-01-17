from movies_data import Movies
from data_visualisation import *

year = int(input("I'll make you a movie raport. Which year are you interested in? "))

data = Movies.popular_movies(year)
# df = create_movie_table(data)
# Movies.avg_rating(data) - # srednia
# print(plot_movie_ratings(df))
#print(top3_reviews_table(Movies.movies_with_reviews(year))) # top3 with reviews
