from movies_data import Movies
from data_visualisation import Visualization
from fpdf import FPDF 
from io import BytesIO
import pandas as pd

year = int(input("I'll make you a movie raport. Which year are you interested in? "))

def add_table_to_pdf(pdf, dataframe, title, x=10, y=30):
    pdf.set_font("Arial", size=16, style='B')
    pdf.cell(200, 10, txt=title, ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    
    if isinstance(dataframe, pd.Series):
        dataframe = dataframe.reset_index()
        dataframe.columns = ['Country', 'Movies Count']

    # width of column since we want it to wrap the text inside
    col_widths = [max(pdf.get_string_width(str(val)) for val in dataframe[col]) + 10 for col in dataframe.columns]
    
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

def add_reviews_to_pdf(pdf, data, title="Movies Reviews", x=10, y=30):
    pdf.set_font("Arial", size=16, style='B')
    pdf.cell(200, 10, txt=title, ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", size=12)

    for movie in data:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt=f"Title: {movie['Title']}", ln=True)
        
        pdf.set_font("Arial", size=10)
        
        review1 = movie['Review 1'] if movie['Review 1'] != "No review available" else " "
        pdf.multi_cell(0, 10, txt=f"Review 1: {review1}")
        
        review2 = movie['Review 2'] if movie['Review 2'] != "No review available" else " "
        pdf.multi_cell(0, 10, txt=f"Review 2: {review2}")
        
        pdf.ln(5)

def generate_pdf(filename="data_analysis.pdf"):
    # Tworzymy obiekt PDF
    pdf = FPDF()
    pdf.add_page()
    data = Movies.get_movies(year)

    # Ustawienia czcionki
    pdf.set_font("Arial", size=16, style='B')
    pdf.cell(200, 10, txt="Data Analysis", ln=True, align="C")

    # Dodanie tekstu w jednej linii
    pdf.set_font("Arial", size=14)  # Poprawiona linia
    pdf.cell(200, 10, txt=Movies.avg_rating(data), ln=True, align="L")

    # Generowanie wykresów
    c = Movies.get_movies_by_country(data)
    df1 = Visualization.movies_country(c)
    img_buffer1 = Visualization.plot_country_distribution(df1)

    #df2 = Visualization.top3_reviews_table(Movies.movies_with_reviews(year))
    #img_buffer2 = Visualization.plot_movie_ratings(df2)

    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt=Movies.avg_rating(data), ln=True, align="L")

    # Dodanie pierwszego wykresu
    pdf.ln(10)  # Zwiększenie odstępu przed wykresem
    pdf.image(img_buffer1, x=10, y=pdf.get_y(), w=180)
    pdf.ln(90)

    # Dodanie drugiego wykresu
    # pdf.ln(90)  # Odstęp między wykresami
    # pdf.image(img_buffer2, x=10, y=pdf.get_y(), w=180)

    pdf.ln(90)
    c = Movies.get_movies_by_country(data)
    add_table_to_pdf(pdf, Visualization.movies_country(c), 'Country Distribution of Movies')

    add_reviews_to_pdf(pdf, Movies.movies_with_reviews(year))

    pdf.ln(90)
    add_table_to_pdf(pdf, Visualization.create_movie_table(data), 'Popular Movies')

    pdf.output(filename)



generate_pdf()

#print(Visualization.top3_reviews_table(Movies.movies_with_reviews(year)))
