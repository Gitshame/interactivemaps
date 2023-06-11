from dataclasses import dataclass

from pydantic import BaseModel
import typing


class MapBase(BaseModel):
    name: str
    game: typing.Optional[str]
    description: typing.Optional[str]
    image: typing.Optional[str]
    x_dimension: int
    y_dimension: int


class MapCreate(MapBase):
    pass


class Map(MapBase):
    id: int
    author: str

    class Config:
        orm_mode = True


class MapUpdate(MapBase):
    pass


class MapLayerBase(BaseModel):
    name: str
    description: typing.Optional[str]
    image: typing.Optional[str]
    priority: int
    public: bool = False


class MapLayerCreate(MapLayerBase):
    pass


class MapLayer(MapLayerBase):
    id: int
    map_id: int
    author: str

    class Config:
        orm_mode = True


class MapLayerUpdate(MapLayerCreate):
    pass


class MapDetails(Map):
    layers: typing.List[MapLayer]


class MapPointBase(BaseModel):
    name: str
    description: typing.Optional[str]
    image: typing.Optional[str]
    x_position: int
    y_position: int


class MapPointCreate(MapPointBase):
    pass


class MapPoint(MapPointBase):
    id: int
    map_layer_id: int
    author: int

    class Config:
        orm_mode = True


class MapLayerDetails(MapLayer):
    points: typing.List[MapPoint]


class UserData(BaseModel):
    user: typing.Dict
    roles: typing.List


class MapGroupBase(BaseModel):
    discord_group_id: int
    display_name: str


class MapGroupCreate(MapGroupBase):
    pass


class MapGroup(MapGroupBase):
    id: int

@dataclass
class LayerPermission:
    read: bool
    create: bool
    delete: bool
    modify: bool