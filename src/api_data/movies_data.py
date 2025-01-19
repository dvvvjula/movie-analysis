from dotenv import load_dotenv
import os
import requests
from exceptions.exceptions import MoviesInfoError

class Movies:
    load_dotenv()
    api_key = os.getenv("API_KEY")

    @staticmethod
    def get_movies(year:int):
        if year < 2000:
            raise MoviesInfoError("Year has to be at least 2000, sorry!")
        response = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={Movies.api_key}&primary_release_year={year}")
        data = response.json()
        return data

    @staticmethod
    def get_movie_country(movie_id: int):
        response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={Movies.api_key}")
        movie_data = response.json()
        return movie_data
    
    @staticmethod
    def get_movies_by_country(data):
        movies = data['results']
        countries = []

        for movie in movies:
            movie_id = movie['id']
            movie_details = Movies.get_movie_country(movie_id)
            
            production_countries = movie_details.get('production_countries', [])
            if production_countries:
                for country in production_countries:
                    countries.append(country['name'])
        return countries

    @staticmethod
    def get_movie_reviews(movie_id: int):
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key={Movies.api_key}&language=en-US"
        response = requests.get(url)
    
        if response.status_code == 200:
            reviews = response.json().get('results', [])
            return [review['content'] for review in reviews[:3]]

    @staticmethod
    def movies_with_reviews(year):
        response = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={Movies.api_key}&year={year}&sort_by=popularity.desc")
        
        data = response.json()
        movies = data['results']
        movie_list = []

        for movie in movies[:3]: # top 3
            movie_id = movie['id']
            reviews = Movies.get_movie_reviews(movie_id)

            movie_dict = {
                'Title': movie['title'],
                'Review 1': reviews[0] if len(reviews) > 0 else 'No review available',
                'Review 2': reviews[1] if len(reviews) > 1 else 'No review available'
            }
            movie_list.append(movie_dict)
        
        return movie_list

    @staticmethod
    def avg_rating(data)->str:
        movies = data['results']
    
        total_rating = 0
        total_movies = 0
        
        for movie in movies:
            if 'vote_average' in movie:
                total_rating += int(movie['vote_average'])
                total_movies += 1
        
        average = total_rating / total_movies
        return f"Average rating: {average:.2f}"
    
    @staticmethod
    def best_movie(data)->str:
        best_movie = max(data['results'], key=lambda movie: movie.get('vote_average', 0))
        title = best_movie['title']
        rating = best_movie.get('vote_average', 0)

        return f"Best movie was '{title}' with an average rating of {rating}"

    @staticmethod
    def worst_movie(data)->str:
        worst_movie = min(data['results'], key=lambda movie: movie.get('vote_average', 0))
        title = worst_movie['title']
        rating = worst_movie.get('vote_average', 0)

        return f"Worst movie was '{title}' with an average rating of {rating}"
