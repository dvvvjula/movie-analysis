from raport.create_raport import Raport

year = int(input("I'll make you a movie raport. Which year are you interested in? "))
try:
    Raport.generate_pdf(year)
except Exception as e:
    print(f"ERROR!\n{e}")


