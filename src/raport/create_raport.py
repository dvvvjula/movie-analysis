from api_data.movies_data import Movies
from raport.data_visualization import Visualization
from fpdf import FPDF 
import pandas as pd

class Raport:
    @staticmethod
    def add_table_to_pdf(pdf, dataframe, title, x=10, y=30):
        pdf.set_font('ArialUnicode', '', 16)
        pdf.cell(200, 10, txt=title, ln=True, align="C")
        pdf.ln(10)

        pdf.set_font('ArialUnicode', '', 10)
        
        # otherwise there's a Series object error...
        if isinstance(dataframe, pd.Series):
            dataframe = dataframe.reset_index()
            dataframe.columns = ['Country', 'Movies Count']

        # width of column to wrap the text inside
        col_widths = [
            max(pdf.get_string_width(str(val)) for val in [col] + list(dataframe[col])) + 10
            for col in dataframe.columns
        ]
        
        # headers
        pdf.set_fill_color(200, 220, 255)
        for col, width in zip(dataframe.columns, col_widths):
            pdf.cell(width, 10, col, border=1, align='C', fill=True)
        pdf.ln()

        pdf.set_fill_color(255, 255, 255)
        for i in range(len(dataframe)):
            for col, width in zip(dataframe.columns, col_widths):
                pdf.cell(width, 10, str(dataframe.iloc[i][col]), border=1, align='C', fill=True)
            pdf.ln()

    @staticmethod
    def add_reviews_to_pdf(pdf, data, title="Movies Reviews", x=10, y=30):
        pdf.set_font('ArialUnicode', '', 16)
        pdf.cell(200, 10, txt=title, ln=True, align="C")
        pdf.ln(10)

        pdf.set_font("Arial", size=12)

        for movie in data:
            pdf.set_font('ArialUnicode', '', 12)
            pdf.cell(200, 10, txt=f"Title: {movie['Title']}", ln=True)
            
            pdf.set_font('ArialUnicode', '', 10)
            
            review1 = movie['Review 1'] if movie['Review 1'] != "No review available" else " "
            pdf.multi_cell(0, 10, txt=f"Review 1: {review1}")
            
            review2 = movie['Review 2'] if movie['Review 2'] != "No review available" else " "
            pdf.multi_cell(0, 10, txt=f"Review 2: {review2}")

    @staticmethod
    def generate_pdf(year, filename="data_analysis.pdf"):
        pdf = FPDF()
        pdf.add_page()
        # we will need data variable here for further methods:
        data = Movies.get_movies(year)

        pdf.add_font('ArialUnicode', '', 'src/font/arial_unicode_ms.otf', uni=True)

        pdf.set_font('ArialUnicode', '', 16)
        pdf.cell(200, 10, txt=f"{year} Movie Data Analysis", ln=True, align="C")

        # introduction (avg, best, worst rating)
        pdf.set_font('ArialUnicode', '', 14)
        pdf.cell(200, 10, txt=Movies.avg_rating(data), ln=True, align="L")
        pdf.cell(200, 10, txt=Movies.best_movie(data), ln=True, align="L")
        pdf.cell(200, 10, txt=Movies.worst_movie(data), ln=True, align="L")

        # 1st diagram's img:
        c = Movies.get_movies_by_country(data)
        df1 = Visualization.movies_country(c)
        img_buffer1 = Visualization.plot_country_distribution(df1)

        # 2nd diagram's img:
        df2 = Visualization.create_movie_table(data)
        img_buffer2 = Visualization.plot_movie_ratings(df2)

        # popular movies ratings diagram 
        pdf.ln(10)
        pdf.set_font('ArialUnicode', '', 14)
        pdf.cell(200, 10, txt=f"Popular Movies Rating", ln=True, align="C")
        pdf.image(img_buffer2, x=10, y=pdf.get_y(), w=180)

        # popular movies table of each movie info
        pdf.ln(120)
        Raport.add_table_to_pdf(pdf, Visualization.create_movie_table(data), 'Popular Movies')

        # movies of the year, country of origin diagram
        pdf.ln(30)
        pdf.set_font('ArialUnicode', '', 14)
        pdf.cell(200, 10, txt=f"Number of Movies per Country", ln=True, align="C")
        pdf.image(img_buffer1, x=10, y=pdf.get_y(), w=180)

        # movies of the year table of each country and its movie count
        pdf.ln(90)
        c = Movies.get_movies_by_country(data)
        Raport.add_table_to_pdf(pdf, Visualization.movies_country(c), 'Country Distribution of Movies')

        # some top3 movies reviews
        pdf.ln(30)
        Raport.add_reviews_to_pdf(pdf, Movies.movies_with_reviews(year))

        pdf.output(filename)