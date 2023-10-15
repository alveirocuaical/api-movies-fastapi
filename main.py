from typing import Any, Coroutine, Optional
from fastapi import FastAPI, Body, Path, Query, status, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.requests import Request
import uvicorn
from schemas.movie import Movie
from jwt_manager import create_token, validate_token
from schemas.user import User
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder



app = FastAPI()
app.title = 'MY FASTAPI APLICATION'
app.version = "0.0.1"


Base.metadata.create_all(engine)

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'
    },
    {
        'id': 2,
        'title': 'Avatar 2',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2023',
        'rating': 7.8,
        'category': 'Acción'
    }
]

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth =  await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@mail.com":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid user")

#================================================
# login

@app.post('/login', tags=['Authentication'])
def login(user : User):
    if user.email == "admin@mail.com" and user.password == "admin":
        token = create_token(user.model_dump())
        return JSONResponse(content={'token': token}, status_code=200)
    return JSONResponse(content={'message': 'Invalid credentials'}, status_code=401)

#================================================




@app.get('/', tags=['Home'])
def message():
    return HTMLResponse('<h1> hello </h1>')

@app.get('/movies', tags=['Movies'], response_model=list[Movie], dependencies=[Depends(JWTBearer)])
def get_movies() -> list[Movie]:
    db = Session()
    movies_found = db.query(MovieModel).all()
    
    return JSONResponse(content=jsonable_encoder(movies_found), status_code=status.HTTP_200_OK)

@app.get('/movies{id}', tags=['Movies'])
def get_movie(id: int = Path(ge = 1, le= 2000)):
        db = Session()
        movie_by_id = db.query(MovieModel).filter(MovieModel.id == id).first()
        return JSONResponse(content=jsonable_encoder(movie_by_id), status_code=200)  if movie_by_id else  JSONResponse(content={'message': 'Movie not found'}, status_code=status.HTTP_204_NO_CONTENT)


@app.get('/movies/', tags=['Movies'], response_model=list[Movie])
def get_movies(category: str = Query(min_length=5 , max_length=20) ) -> list[Movie]:
    db = Session()
    movies_by_category  = db.query(MovieModel).filter(MovieModel.category == category).all()
    return JSONResponse(content=jsonable_encoder(movies_by_category), status_code=status.HTTP_200_OK) if movies_by_category else JSONResponse(content={'message': 'Movie not found'}, status_code=status.HTTP_204_NO_CONTENT)

@app.post('/movies', tags=['Movies'], response_model=dict)
def create_movie(movie : Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.model_dump())
    db.add(new_movie)
    db.commit()
    return JSONResponse(content={"message": "Movie created successfully"}, status_code=status.HTTP_201_CREATED)


@app.put('/movies/{id}', tags=['Movies'])
def update_movie(id : int, movie :Movie):
    db = Session()
    find_movie = db.query(MovieModel).filter(MovieModel.id == id).first()
    find_movie.title = movie.title
    find_movie.overview = movie.overview
    find_movie.year = movie.year
    find_movie.rating = movie.rating
    find_movie.category = movie.category   
    
    db.commit()  
    movie_by_id = db.query(MovieModel).filter(MovieModel.id == id).first()
    return JSONResponse(content=jsonable_encoder(movie_by_id), status_code=200)  if movie_by_id else JSONResponse(content={'message': 'Movie not found'}, status_code=status.HTTP_204_NO_CONTENT)


@app.delete('/movies/{id}', tags=['Movies'], response_model=dict)
def delete_movie(id : int) -> dict:
    db = Session()
    movie = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not movie:
        return {'message': 'Movie not found'}
    #delete movie
    db.delete(movie)
    db.commit()    
    return {'message': 'Movie deleted successfully'}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)
