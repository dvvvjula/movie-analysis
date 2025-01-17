from dotenv import load_dotenv
import os
import requests
from exceptions import MoviesInfoError

class Movies:
    load_dotenv()
    api_key = os.getenv("API_KEY")

    @staticmethod
    def popular_movies(year:int):
        if year < 1960:
            pass
            #raise MoviesInfoError
        response = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={Movies.api_key}&primary_release_year={year}")
        data = response.json()
        return data

    @staticmethod
    def avg_rating(data):
        movies = data['results']
    
        total_rating = 0
        total_movies = 0
        
        # Iteracja po filmach
        for movie in movies:
            # Sprawdzamy, czy film ma ocenę
            if 'vote_average' in movie:
                total_rating += int(movie['vote_average'])
                total_movies += 1
        
        # Sprawdzanie, czy mamy jakiekolwiek filmy
        if total_movies > 0:
            average = total_rating / total_movies
            print(f"Średnia ocena: {average:.2f}")
        else:
            print("Brak filmów z ocenami.")
