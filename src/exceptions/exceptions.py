class MoviesInfoError(Exception):
    def __init__(self, message:str="Wrong input, try again please!"):
        super().__init__(message)