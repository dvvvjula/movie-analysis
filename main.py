from raport.create_raport import Raport

year = int(input("I'll make you a movie raport. Which year are you interested in? "))
Raport.generate_pdf(year)


