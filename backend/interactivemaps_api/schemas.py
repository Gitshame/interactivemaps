from pydantic import BaseModel
import typing

class MapBase(BaseModel):
    name: str
    game: typing.Optional[str]
    description: typing.Optional[str]
    image: typing.Optional[str]
    author: str

class MapCreate(MapBase):
    pass

class Map(MapBase):
    id: int
    class Config:
        orm_mode = True

class MapLayerBase(BaseModel):
    name: str
    description: typing.Optional[str]
    image: typing.Optional[str]

class MapLayerCreate(MapLayerBase):
    pass

class MapLayer(MapLayerBase):
    id: int
    map_id: int

    class Config:
        orm_mode = True

class MapPointBase(BaseModel):
    name: str
    description: typing.Optional[str]
    image: typing.Optional[str]

class MapPointCreate(MapPointBase):
    pass

class MapPoint(MapPointBase):
    id: int
    map_layer_id: int

    class Config:
        orm_mode = True