from sqlalchemy.orm import Session
from . import models, schemas

def get_map(db: Session, map_id: int) -> models.Map:
    return db.query(models.Map).filter(models.Map.id == map_id).first()

def get_maps(db: Session) -> list[models.Map]:
    return db.query(models.Map).all()