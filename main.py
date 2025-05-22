from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.config import settings
from app.database import get_db, create_tables

from app.models.cinema import Cinema, Sala
from app.models.filme import Filme
from app.models.Produto import Produto, Pagamento
from app.models.reserva import Reserva, ItemReserva
from app.models.sessao import Sessao, Assento
from app.models.usuario import Usuario, Endereco

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION,
)

@app.on_event("startup")
async def startup_event():
    try:
        create_tables()
        print("Tables created successfully.")
        print(f"Database connection established: {settings.DATABASE_URL}")
    except Exception as e:
        print(f"Error creating tables: {str(e)}")

@app.get("/")
def read_root():
    return {
        "message": "Cinema API is working!",
        "version": settings.PROJECT_VERSION,
        "project": settings.PROJECT_NAME
    }

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1"))
        result.scalar()
        return {
            "status": "healthy", 
            "database": "connected",
            "message": "Database connection is successful"
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "error": str(e),
                "message": "Database connection failed"
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)