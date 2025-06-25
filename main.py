import app.models

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.config import settings
from app.database import get_db, create_tables, initialize_database

from app.controllers.usuario_controller import router as usuario_router
from app.controllers.endereco_controller import router as endereco_router
from app.controllers.cinema_controller import router as cinema_router
from app.controllers.produto_controller import router as produto_router
from app.controllers.sala_controller import router as sala_router
from app.controllers.filme_controller import router as filme_router
from app.controllers.sessao_controller import router as sessao_router
from app.controllers.reserva_controller import router as reserva_router
from app.controllers.item_reserva_controller import router as item_reserva_router
from app.controllers.payment_controller import router as pagamento_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION,
)

app.include_router(usuario_router, prefix="/api/v1", tags=["Users"])
app.include_router(endereco_router, prefix="/api/v1", tags=["Address"])
app.include_router(cinema_router, prefix="/api/v1", tags=["Cinema"])
app.include_router(produto_router, prefix="/api/v1", tags=["Products"])
app.include_router(sala_router, prefix="/api/v1", tags=["Room"])
app.include_router(filme_router, prefix="/api/v1", tags=["Movies"])
app.include_router(sessao_router, prefix="/api/v1", tags=["Session"])
app.include_router(reserva_router, prefix="/api/v1", tags=["Reservation"])
app.include_router(item_reserva_router, prefix="/api/v1", tags=["Reservation Items"])
app.include_router(pagamento_router, prefix="/api/v1", tags=["Payment"])

@app.on_event("startup")
async def startup_event():
    try:
        # create_tables()
        initialize_database()
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