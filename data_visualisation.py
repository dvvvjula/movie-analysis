from movies_data import Movies
import pandas as pd
import matplotlib.pyplot as plt

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

def top3_reviews_table(data):
    df = pd.DataFrame(data)
    return df

def movies_country(data):    
    country_counts = pd.Series(data).value_counts()
    return country_counts

def plot_country_distribution(country_counts):
    plt.figure(figsize=(10, 6))
    country_counts.head(10).plot(kind='bar', color='skyblue')
    plt.title('Number of Movies per Country')
    plt.xlabel('Country')
    plt.ylabel('Number of Movies')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def plot_movie_ratings(df):
    plt.figure(figsize=(10, 6))
    plt.barh(df['Title'], df['Rating'], color='maroon')
    plt.xlabel('Rating')
    plt.title('Popular Movies Ratings')
    plt.show()