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
        movie = [movie for movie in movies if movie['id'] == id]
        return JSONResponse(content=movie[0], status_code=200)  if movie else JSONResponse(content={'message': 'Movie not found'}, status_code=status.HTTP_204_NO_CONTENT)


@app.get('/movies/', tags=['Movies'], response_model=list[Movie])
def get_movies(category: str = Query(min_length=5 , max_length=20) ) -> list[Movie]:
    movies_by_category  = [movie for movie in movies if movie['category'] == category]
    return JSONResponse(content=movies_by_category, status_code=status.HTTP_200_OK) if movies_by_category else JSONResponse(content={'message': 'Movie not found'}, status_code=status.HTTP_204_NO_CONTENT)

@app.post('/movies', tags=['Movies'], response_model=dict)
def create_movie(movie : Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.model_dump())
    db.add(new_movie)
    db.commit()
    return JSONResponse(content={"message": "Movie created successfully"}, status_code=status.HTTP_201_CREATED)


@app.put('/movies/{id}', tags=['Movies'])
def update_movie(id : int, movie :Movie):
    find_movie = [find_movie for find_movie in movies if find_movie['id'] == id]
    update = {
        'title': movie.title,
        'overview': movie.overview,
        'year': movie.year,
        'rating': movie.rating,
        'category': movie.category
        }
    find_movie[0].update(update)
    return find_movie[0]


@app.delete('/movies/{id}', tags=['Movies'], response_model=dict)
def delete_movie(id : int) -> dict:
    movie = [movie for movie in movies if movie['id'] == id]
    if movie == []:
        return {'message': 'Movie not found'}
    movies.remove(movie[0])
    return {'message': 'Movie deleted successfully'}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)
