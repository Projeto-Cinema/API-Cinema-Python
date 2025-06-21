from fastapi import HTTPException, status
from passlib.context import CryptContext

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.filme import Filme
from app.models.genero import Genero
from app.models.schemas.filme_schema import FilmeCreate

class FilmeService:
    def __init__(self):
        self.pwd_context = CryptContext(deprecated="auto")

    def create_movie(self, db: Session, movie_data: FilmeCreate) -> Filme:
        try:
            movie_dict = movie_data.model_dump(exclude={'generos_id'})
            generos_id = movie_data.generos_id

            db_movie = Filme(**movie_dict)
            db.add(db_movie)
            db.commit()
            db.refresh(db_movie)

            generos = db.query(Genero).filter(Genero.id.in_(generos_id)).all()

            if len(generos) != len(generos_id):
                found_ids = [g.id for g in generos]
                not_found_ids = [gid for gid in generos_id if gid not in found_ids]
                raise ValueError(f"Gêneros não encontrados: {not_found_ids}")
            
            db_movie.generos = generos
            db.commit()
            db.refresh(db_movie)

            return db_movie
        
        except IntegrityError as e:
            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao criar filme."
            )
        
filme_service = FilmeService()