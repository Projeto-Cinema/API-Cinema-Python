from typing import List, Optional

from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.models import Filme
from app.models.genero import Genero
from app.models.schemas.filme_schema import FilmeCreate, FilmeUpdate


class FilmeService:
    def __init__(self):
        self.pwd_context = CryptContext(deprecated="auto")

    def create_movie(self, db: Session, movie_data: FilmeCreate) -> Filme:
        try:
            movie_dict = movie_data.model_dump(exclude={"generos_id"})
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
                detail="Erro ao criar filme.",
            )

    def get_movie_by_id(self, db: Session, movie_id: int) -> Optional[Filme]:
        return db.query(Filme).filter(Filme.id == movie_id).first()

    def get_movie_by_title(self, db: Session, title: str) -> Optional[Filme]:
        return db.query(Filme).filter(func.lower(Filme.titulo) == title.lower()).first()

    def get_all_movies(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        em_cartaz: Optional[bool] = None,
        diretor: Optional[str] = None,
        classificacao: Optional[str] = None,
        ano_lancamento: Optional[int] = None,
    ) -> List[Filme]:
        query = db.query(Filme).options(joinedload(Filme.generos))

        if em_cartaz is not None:
            query = query.filter(Filme.em_cartaz == em_cartaz)

        if diretor is not None:
            query = query.filter(Filme.diretor.ilike(f"%{diretor}%"))

        if classificacao is not None:
            query = query.filter(Filme.classificacao.ilike(f"%{classificacao}%"))

        if ano_lancamento is not None:
            query = query.filter(Filme.ano_lancamento == ano_lancamento)

        return query.offset(skip).limit(limit).all()

    def update_movie(
        self, db: Session, movie_id: int, movie_data: FilmeUpdate
    ) -> Optional[Filme]:
        db_movie = self.get_movie_by_id(db, movie_id)

        if not db_movie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Filme não encontrado."
            )

        try:
            movie_dict = movie_data.model_dump(
                exclude_unset=True, exclude={"generos_id"}
            )

            for key, value in movie_dict.items():
                setattr(db_movie, key, value)

            db.add(db_movie)
            db.commit()
            db.refresh(db_movie)

            return db_movie

        except IntegrityError as e:
            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao atualizar filme.",
            )

    def delete_permanent_movie(self, db: Session, movie_id: int) -> bool:
        db_movie = self.get_movie_by_id(db, movie_id)

        if not db_movie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Filme não encontrado."
            )

        db.delete(db_movie)
        db.commit()

        return True


filme_service = FilmeService()
