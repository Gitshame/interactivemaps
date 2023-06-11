from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from .database import Base

class InteractiveMap(Base):
    __tablename__ = 'maps'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    game = Column(String)
    description = Column(String)
    image = Column(String)
    author = Column(Integer, ForeignKey('users.id'))
    x_dimension = Column(Integer)
    y_dimension = Column(Integer)

class InteractiveMapLayer(Base):
    __tablename__ = 'map_layers'

    id = Column(Integer, primary_key=True, index=True)
    map_id = Column(Integer, ForeignKey('maps.id'))
    name = Column(String)
    description = Column(String)
    image = Column(String)
    author = Column(String)
    priority = Column(Integer)
    public = Column(Boolean)

class InteractiveMapPoint(Base):
    __tablename__ = 'map_points'

    id = Column(Integer, primary_key=True, index=True)
    map_layer_id = Column(Integer, ForeignKey('map_layers.id'))
    name = Column(String)
    description = Column(String)
    image = Column(String)
    author = Column(String)
    x_position = Column(Integer)
    y_position = Column(Integer)

class InteractiveMapUser(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    discord_id = Column(Integer)
    display_name = Column(String)
    admin = Column(Boolean, default=False)

class InteractiveMapGroup(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, index=True)
    discord_group_id = Column(Integer)
    display_name = Column(String)

class InteractiveMapUserPermission(Base):
    __tablename__ = 'user_permissions'

    id = Column(Integer, primary_key=True, index=True)
    map_layer_id = Column(Integer, ForeignKey('map_layers.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    read = Column(Boolean)
    create = Column(Boolean)
    delete = Column(Boolean)
    modify = Column(Boolean)

class InteractiveMapGroupPermission(Base):
    __tablename__ = 'group_permissions'

    id = Column(Integer, primary_key=True, index=True)
    map_layer_id = Column(Integer, ForeignKey('map_layers.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))
    read = Column(Boolean)
    create = Column(Boolean)
    delete = Column(Boolean)
    modify = Column(Boolean)