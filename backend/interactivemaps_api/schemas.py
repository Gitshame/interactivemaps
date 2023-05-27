# import pydantic Basemodel
from pydantic import BaseModel

class MapBase(BaseModel):
    name: str
    game: Optional[str]
    description: Optional[str]
    image: Optional[str]
    author: str

class MapCreate(MapBase):
    pass

class Map(MapBase):
    id: int
    class Config:
        orm_mode = True

class MapInDBBase(MapBase):
    id: int

class MapLayerBase(BaseModel):
    name: str
    description: Optional[str]
    image: Optional[str]

class MapLayerCreate(MapLayerBase):
    pass

class MapLayer(MapLayerBase):
    id: int
    map_id: int

    class Config:
        orm_mode = True

class MapPointBase(BaseModel):
    name: str
    description: Optional[str]
    image: Optional[str]

class MapPointCreate(MapPointBase):
    pass

class MapPoint(MapPointBase):
    id: int
    map_layer_id: int

    class Config:
        orm_mode = True