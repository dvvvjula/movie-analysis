from movies_data import Movies

year = int(input("I'll make you a movie raport. Which year are you interested in? "))

data = Movies.popular_movies(year)
Movies.avg_rating(data)