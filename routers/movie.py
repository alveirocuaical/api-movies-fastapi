from fastapi import APIRouter
from schemas.movie import Movie
from fastapi import Path, Query, status, Depends
from fastapi.responses import JSONResponse
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_middleware import JWTBearer
from services.movie_service import MovieService



movie_router = APIRouter()


@movie_router.get('/movies', tags=['Movies'], response_model=list[Movie], dependencies=[Depends(JWTBearer)])
def get_movies() -> list[Movie]: # type: ignore
    db = Session()
    movies_found = MovieService(db).get_movies()
    return JSONResponse(content=jsonable_encoder(movies_found), status_code=status.HTTP_200_OK) # type: ignore

@movie_router.get('/movies{id}', tags=['Movies'])
def get_movie(id: int = Path(ge = 1, le= 2000)):
        db = Session()
        movie_by_id = MovieService(db).get_movie_by_id(movie_id=id)
        return JSONResponse(content=jsonable_encoder(movie_by_id), status_code=200)  if movie_by_id else  JSONResponse(content={'message': 'Movie not found'}, status_code=status.HTTP_204_NO_CONTENT)


@movie_router.get('/movies/', tags=['Movies'], response_model=list[Movie])
def get_movies(category: str = Query(min_length=5 , max_length=20) ) -> list[Movie]:
    db = Session()
    movies_by_category  = MovieService(db).get_movies_by_category(category=category)
    return JSONResponse(content=jsonable_encoder(movies_by_category), status_code=status.HTTP_200_OK) if movies_by_category else JSONResponse(content={'message': 'Movie not found'}, status_code=status.HTTP_204_NO_CONTENT) # type: ignore

@movie_router.post('/movies', tags=['Movies'], response_model=dict)
def create_movie(movie : Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)    
    return JSONResponse(content={"message": "Movie created successfully"}, status_code=status.HTTP_201_CREATED) # type: ignore


@movie_router.put('/movies/{id}', tags=['Movies'])
def update_movie(id : int, movie :Movie):
    db = Session()    
    MovieService(db).update_movie(movie=movie, movie_id=id)
    movie_by_id = db.query(MovieModel).filter(MovieModel.id == id).first()
    return JSONResponse(content=jsonable_encoder(movie_by_id), status_code=200)  if movie_by_id else JSONResponse(content={'message': 'Movie not found'}, status_code=status.HTTP_204_NO_CONTENT)


@movie_router.delete('/movies/{id}', tags=['Movies'], response_model=dict)
def delete_movie(id : int) -> dict:
    db = Session()
    movie = MovieService(db).get_movie_by_id(movie_id=id)
    if not movie:
        return {'message': 'Movie not found'}
    #delete movie   
    MovieService(db).delete_movie(movie_id=id)
    return {'message': 'Movie deleted successfully'}


