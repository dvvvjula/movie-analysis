from api_data.movies_data import Movies
import pandas as pd
import matplotlib.pyplot as plt

class Visualization:

    @staticmethod
    def create_movie_table(data):
        movies = data['results']
        movie_list = []
        
        for movie in movies:
            movie_list.append({
                'Title': movie['title'],
                'Rating': round(movie.get('vote_average', 0),2),
                'Release Date': movie['release_date'],
            })
        
        df = pd.DataFrame(movie_list)
        return df

    @staticmethod
    def movies_country(data):    
        country_counts = pd.Series(data).value_counts()
        return country_counts
    
    @staticmethod
    def top3_reviews_table(data):
        df = pd.DataFrame(data)
        return df

    @staticmethod
    def plot_country_distribution(df):
        plt.figure(figsize=(10, 6))
        df.head(10).plot(kind='bar', color='maroon')
        plt.title('Number of Movies per Country')
        plt.xlabel('Country')
        plt.ylabel('Number of Movies')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        # for pdf raport later on:
        plot_file = "country_distribution.png"
        plt.savefig(plot_file)
        plt.close()

        return plot_file

    @staticmethod
    def plot_movie_ratings(df):
        plt.figure(figsize=(10, 6))
        plt.barh(df['Title'], df['Rating'], color='maroon')
        plt.xlabel('Rating')
        plt.title('Popular Movies Ratings')

        # for pdf raport later on:
        plot_file = "movie_ratings.png"
        plt.savefig(plot_file)
        plt.close()

        return plot_file