from sqlalchemy.orm import Session
from . import models, schemas

def get_map(db: Session, map_id: int) -> models.InteractiveMap:
    return db.query(models.InteractiveMap).filter(models.Map.id == map_id).first()

def get_maps(db: Session) -> list[models.InteractiveMap]:
    return db.query(models.InteractiveMap).all()