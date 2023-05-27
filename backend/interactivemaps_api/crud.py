from sqlalchemy.orm import Session
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

    db.commit()
    db.refresh(current_map)

    return current_map