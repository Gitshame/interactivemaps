from sqlalchemy.orm import Session
from . import models, schemas

def get_map(db: Session, map_id: int) -> models.InteractiveMap:
    return db.query(models.InteractiveMap).filter(models.InteractiveMaps.id == map_id).first()

def get_maps(db: Session) -> list[models.InteractiveMap]:
    return db.query(models.InteractiveMap).all()

def create_map(db: Session, map: schemas.InteractiveMapCreate) -> models.InteractiveMap:
    db_map = models.InteractiveMap(**map.dict())
    db.add(db_map)
    db.commit()
    db.refresh(db_map)
    return db_map