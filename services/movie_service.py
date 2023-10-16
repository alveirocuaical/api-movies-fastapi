from models.movie import Movie as MovieModel


class MovieService():
    
    def __init__(self, db) -> None:
        self.db = db
        
    def get_movies(self):
       result =  self.db.query(MovieModel).all()
       return result
   
    def get_movie_by_id(self, movie_id):
       result = self.db.query(MovieModel).filter(MovieModel.id == movie_id).first()
       return result
   
    def get_movies_by_category(self, category : str):
       result = self.db.query(MovieModel).filter(MovieModel.category == category).all()
       return result
   
    def create_movie(self, movie):
       new_movie = MovieModel(**movie.model_dump())
       self.db.add(new_movie)
       self.db.commit()
       return       
   
    def update_movie(self, movie, movie_id):
        find_movie = self.get_movie_by_id(movie_id)
        find_movie.title = movie.title
        find_movie.overview = movie.overview
        find_movie.year = movie.year
        find_movie.rating = movie.rating
        find_movie.category = movie.category           
        self.db.commit()
        return 
    
    def delete_movie(self, movie_id):
        find_movie = self.get_movie_by_id(movie_id)
        self.db.delete(find_movie)
        self.db.commit()
        return