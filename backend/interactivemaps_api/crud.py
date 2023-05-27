from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas

def get_map(db: Session, map_id: int) -> models.InteractiveMap:
    return db.query(models.InteractiveMap).filter(models.InteractiveMap.id == map_id).first()

def get_maps(db: Session) -> list[models.InteractiveMap]:
    return db.query(models.InteractiveMap).all()

def create_map(db: Session, map: schemas.MapCreate) -> models.InteractiveMap:
    db_map = models.InteractiveMap(**map.dict())
    db.add(db_map)
    db.commit()
    db.refresh(db_map)
    return db_map

def update_map(db: Session, map_id: int, map: schemas.MapCreate) -> models.InteractiveMap:
    current_map = get_map(db, map_id)
    if current_map is None:
        raise HTTPException(status_code=404, detail="Map not found")
    current_map.name = map.name or current_map.name
    current_map.description = map.description or current_map.description
    current_map.game = map.game or current_map.game
    current_map.image = map.image or current_map.image
    current_map.x_dimension = map.x_dimension or current_map.x_dimension
    current_map.y_dimension = map.y_dimension or current_map.y_dimension

    db.commit()
    db.refresh(current_map)

    return current_map

def get_map_layer(db: Session, map_id: int, layer_id: int) -> models.InteractiveMapLayer:
    return db.query(models.InteractiveMapLayer).filter(models.InteractiveMapLayer.map_id == map_id, models.InteractiveMapLayer.id == layer_id).first()

def get_map_layers(db: Session, map_id: int) -> list[models.InteractiveMapLayer]:
    return db.query(models.InteractiveMapLayer).filter(models.InteractiveMapLayer.map_id == map_id).all()

def create_map_layer(db: Session, map_id: int, map_layer: schemas.MapLayerCreate) -> models.InteractiveMapLayer:
    db_map_layer = models.InteractiveMapLayer(**map_layer.dict(), map_id=map_id)
    db.add(db_map_layer)
    db.commit()
    db.refresh(db_map_layer)
    return db_map_layer

def update_map_layer(db: Session, map_id: int, layer_id: int, map_layer: schemas.MapLayerCreate) -> models.InteractiveMapLayer:
    current_map_layer = get_map_layer(db, map_id, layer_id)
    if current_map_layer is None:
        raise HTTPException(status_code=404, detail="Layer not found")
    current_map_layer.name = map_layer.name or current_map_layer.name
    current_map_layer.description = map_layer.description or current_map_layer.description
    current_map_layer.image = map_layer.image or current_map_layer.image
    current_map_layer.author = map_layer.author or current_map_layer.author

    db.commit()
    db.refresh(current_map_layer)

    return current_map_layer

def get_map_points(db: Session, map_id: int, map_layer_id: int) -> list[models.InteractiveMapPoint]:
    return db.query(models.InteractiveMapPoint).filter(models.InteractiveMapPoint.map_layer_id == map_layer_id).all()

def create_map_point(db: Session, map_id: int, map_layer_id: int, map_point: schemas.MapPointCreate) -> models.InteractiveMapPoint:
    db_map_point = models.InteractiveMapPoint(**map_point.dict(), map_layer_id=map_layer_id)
    db.add(db_map_point)
    db.commit()
    db.refresh(db_map_point)
    return db_map_point