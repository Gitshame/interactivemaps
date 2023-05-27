import typing
from fastapi import FastAPI, Depends, HTTPException
from .database import SessionLocal, engine
from . import crud, models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/maps", response_model=typing.List[schemas.Map])
def route_get_maps(db = Depends(get_db)):
    maps = crud.get_maps(db)
    return maps

@app.post("/maps", response_model=schemas.Map)
def route_create_map(map: schemas.MapCreate, db = Depends(get_db)):
    return crud.create_map(db, map)

@app.patch("/maps/{map_id}", response_model=schemas.Map)
def route_update_map(map_id: int, map: schemas.MapUpdate, db = Depends(get_db)):
    return crud.update_map(db, map_id, map)

@app.get("/maps/{map_id}", response_model=schemas.MapDetails)
def route_get_map_details(map_id: int, db = Depends(get_db)):
    response = crud.get_map(db, map_id).__dict__

    response['layers'] = crud.get_map_layers(db, map_id)
    return response

@app.post("/maps/{map_id}/layers", response_model=schemas.MapLayer)
def route_create_layer(map_id: int, layer: schemas.MapLayerCreate, db = Depends(get_db)):
    return crud.create_map_layer(db, map_id, layer)
