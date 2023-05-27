from .database import Base

class InteractiveMap(Base):
    __tablename__ = 'maps'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    game = Column(String)
    description = Column(String)
    image = Column(String)
    author = Column(String)

class InteractiveMapLayer(Base):
    __tablename__ = 'map_layers'

    id = Column(Integer, primary_key=True, index=True)
    map_id = Column(Integer, ForeignKey('maps.id'))
    name = Column(String)
    description = Column(String)
    image = Column(String)
    author = Column(String)

class InteractiveMapPoint(Base):
    __tablename__ = 'map_points'

    id = Column(Integer, primary_key=True, index=True)
    map_layer_id = Column(Integer, ForeignKey('map_layers.id'))
    name = Column(String)
    description = Column(String)
    image = Column(String)
    author = Column(String)