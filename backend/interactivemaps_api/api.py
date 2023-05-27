from fastapi import FastAPI, Depends, HTTPException
from .database import SessionLocal, engine
from . import crud, models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependencies
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/maps", response_model=List[schemas.Map])
def route_get_maps(db: Session = Depends(get_db)):
    maps = crud.get_maps(db)
    return maps