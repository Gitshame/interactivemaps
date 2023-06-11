import os
import typing

from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, Header
from . import models, schemas
from .database import SessionLocal

from jose import jwt

SECRET_KEY = os.environ.get('JWT_TOKEN_SECRET')
ALGORITHM = os.environ.get('JWT_TOKEN_ALGO', "HS256")


# DEPENDENCY INJECTION METHODS
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_map(db: typing.Annotated[Session, Depends(get_db)],
            map_id: int) -> models.InteractiveMap:
    response_map = db.query(models.InteractiveMap).filter(models.InteractiveMap.id == map_id).first()

    if not response_map:
        raise HTTPException(status_code=404, detail='Map not found')

    return response_map


def get_map_layer(db: typing.Annotated[Session, Depends(get_db)],
                  map_id: int,
                  layer_id: int) -> models.InteractiveMapLayer:
    response_layer = db.query(models.InteractiveMapLayer) \
        .filter(models.InteractiveMapLayer.map_id == map_id,
                models.InteractiveMapLayer.id == layer_id) \
        .first()
    if not response_layer:
        raise HTTPException(status_code=404, detail='Layer not found')

    return response_layer


def get_user(db: typing.Annotated[Session, Depends(get_db)],
             authorization: typing.Annotated[str, Header()] = None) -> typing.Optional[schemas.UserData]:
    if not authorization:
        return None

    token = authorization

    token_value = token.split(' ')[1]
    try:
        jwt_data = jwt.decode(token_value, SECRET_KEY, algorithms=[ALGORITHM])

        user = get_user_from_db(db, jwt_data['discord']['id'])

        if not user:
            user = register_user(db, jwt_data['discord']['id'], jwt_data['discord']['username'])

        response = schemas.UserData(user=user.__dict__, roles=jwt_data['discord_groups'])

        return response
    except:
        return None


def get_db_user(db: typing.Annotated[Session, Depends(get_db)],
                user: typing.Annotated[typing.Optional[schemas.UserData], Depends(get_user)]) -> typing.Optional[
    models.InteractiveMapUser]:
    if not user:
        return None
    return get_user_from_db(db, user.user['discord_id'])


def get_user_from_db(db: Session,
                     discord_user_id: int) -> typing.Optional[models.InteractiveMapUser]:
    return db.query(models.InteractiveMapUser).filter(
        models.InteractiveMapUser.discord_id == int(discord_user_id)).first()


def get_groups(user: typing.Annotated[typing.Optional[schemas.UserData], Depends(get_user)],
               db: typing.Annotated[Session, Depends(get_db)]) -> typing.List[models.InteractiveMapGroup]:
    groups = []
    if not user:
        return []

    roles = user.roles
    for i in roles:
        group_obj = get_group(db, i)
        if group_obj:
            groups.append(group_obj)
    return groups


def is_layer_owner(user: typing.Annotated[typing.Optional[schemas.UserData], Depends(get_user)],
                   layer: typing.Annotated[models.InteractiveMapLayer, Depends(get_map_layer)]) -> bool:
    return user.id == layer.author


def is_admin(user: typing.Annotated[models.InteractiveMapUser, Depends(get_db_user)],
             ) -> bool:
    if not user.admin:
        raise HTTPException(status_code=403, detail="Insufficient permission")

    return user.admin


def has_layer_read_permission(user: typing.Annotated[typing.Optional[schemas.UserData], Depends(get_user)],
                              db_user: typing.Annotated[models.InteractiveMapUser, Depends(get_db_user)],
                              layer: typing.Annotated[models.InteractiveMapLayer, Depends(get_map_layer)],
                              groups: typing.Annotated[typing.List[models.InteractiveMapGroup], Depends(get_groups)],
                              db: typing.Annotated[Session, Depends(get_db)]) -> bool:
    if layer.public:
        return True

    user_permissions = get_user_layer_permissions(db, layer.id, db_user.id)
    group_permissions = get_group_layer_permissions(db, layer.id, [i.id for i in groups])

    has_read = user_permissions.read or group_permissions.read or is_admin(db_user)

    if not has_read:
        raise HTTPException(status_code=403, detail='Unable to read layer')

    return has_read


def has_layer_create_permission(user: typing.Annotated[typing.Optional[schemas.UserData], Depends(get_user)],
                                db_user: typing.Annotated[models.InteractiveMapUser, Depends(get_db_user)],
                                layer: typing.Annotated[models.InteractiveMapLayer, Depends(get_map_layer)],
                                groups: typing.Annotated[typing.List[models.InteractiveMapGroup], Depends(get_groups)],
                                db: typing.Annotated[Session, Depends(get_db)]) -> bool:
    user_permissions = get_user_layer_permissions(db, layer.id, db_user.id)
    group_permissions = get_group_layer_permissions(db, layer.id, [i.id for i in groups])

    has_create = user_permissions.create or group_permissions.create or is_admin(db_user)

    if not has_create:
        raise HTTPException(status_code=403, detail='Unable to create point in layer')

    return has_create


def has_layer_modify_permission(user: typing.Annotated[typing.Optional[schemas.UserData], Depends(get_user)],
                                db_user: typing.Annotated[models.InteractiveMapUser, Depends(get_db_user)],
                                layer: typing.Annotated[models.InteractiveMapLayer, Depends(get_map_layer)],
                                groups: typing.Annotated[typing.List[models.InteractiveMapGroup], Depends(get_groups)],
                                db: typing.Annotated[Session, Depends(get_db)]) -> bool:
    user_permissions = get_user_layer_permissions(db, layer.id, db_user.id)
    group_permissions = get_group_layer_permissions(db, layer.id, [i.id for i in groups])

    has_modify = user_permissions.modify or group_permissions.modify or is_admin(db_user)

    if not has_modify:
        raise HTTPException(status_code=403, detail='Unable to modify point in layer')

    return has_modify


def has_layer_delete_permission(user: typing.Annotated[typing.Optional[schemas.UserData], Depends(get_user)],
                                db_user: typing.Annotated[models.InteractiveMapUser, Depends(get_db_user)],
                                layer: typing.Annotated[models.InteractiveMapLayer, Depends(get_map_layer)],
                                groups: typing.Annotated[typing.List[models.InteractiveMapGroup], Depends(get_groups)],
                                db: typing.Annotated[Session, Depends(get_db)]) -> bool:
    user_permissions = get_user_layer_permissions(db, layer.id, db_user.id)
    group_permissions = get_group_layer_permissions(db, layer.id, [i.id for i in groups])

    has_delete = user_permissions.delete or group_permissions.delete or is_admin(db_user)

    if not has_delete:
        raise HTTPException(status_code=403, detail='Unable to delete point in layer')

    return has_delete


def get_user_layer_permissions(db: Session,
                               layer_id: int,
                               user_id: int) -> schemas.LayerPermission:
    permissions: models.InteractiveMapUserPermission = db.query(models.InteractiveMapUserPermission) \
        .filter(models.InteractiveMapUserPermission.map_layer_id == layer_id,
                models.InteractiveMapUserPermission.user_id == user_id).first()

    if permissions:
        return schemas.LayerPermission(read=permissions.read,
                                       create=permissions.create,
                                       modify=permissions.modify,
                                       delete=permissions.delete)
    else:
        return schemas.LayerPermission(read=False,
                                       create=False,
                                       modify=False,
                                       delete=False)


def get_group_layer_permissions(db: Session,
                                layer_id: int,
                                group_ids: typing.List[int]) -> schemas.LayerPermission:
    groups_tuple = tuple(group_ids)
    permissions = db.query(models.InteractiveMapGroupPermission) \
        .filter(models.InteractiveMapGroupPermission.map_layer_id == layer_id,
                models.InteractiveMapGroupPermission.group_id.in_(groups_tuple)).all()

    result_permissions = {
        'read': False,
        'create': False,
        'modify': False,
        'delete': False
    }

    for perm in permissions:
        result_permissions['read'] = result_permissions['read'] or perm.read
        result_permissions['create'] = result_permissions['create'] or perm.create
        result_permissions['modify'] = result_permissions['modify'] or perm.modify
        result_permissions['delete'] = result_permissions['delete'] or perm.delete

    return schemas.LayerPermission(**result_permissions)


def get_layers(db: Session,
               map_id: int) -> typing.List[models.InteractiveMapLayer]:
    return db.query(models.InteractiveMapLayer).filter(models.InteractiveMapLayer.map_id == map_id).all()


def create_map_point(db: Session,
                     db_layer: models.InteractiveMapLayer,
                     map_point: schemas.MapPointCreate,
                     author: models.InteractiveMapUser) -> models.InteractiveMapPoint:
    db_map_point = models.InteractiveMapPoint(**map_point.dict(),
                                              map_layer_id=db_layer.id,
                                              author=author.id)
    db.add(db_map_point)
    db.commit()
    db.refresh(db_map_point)
    return db_map_point


###
# OLD FUNCTIONS, MANUALLY CALLED IN API METHODS
###

def get_maps(db: Session) -> list[models.InteractiveMap]:
    return db.query(models.InteractiveMap).all()


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


def create_map_layer(db: Session,
                     map_id: int,
                     map_layer: schemas.MapLayerCreate,
                     author: int) -> models.InteractiveMapLayer:
    db_map_layer = models.InteractiveMapLayer(**map_layer.dict(), map_id=map_id, author=author)
    db.add(db_map_layer)
    db.commit()
    db.refresh(db_map_layer)
    return db_map_layer


def update_map_layer(db: Session,
                     map_id: int,
                     layer_id: int,
                     map_layer: schemas.MapLayerCreate) -> models.InteractiveMapLayer:
    current_map_layer = get_map_layer(db, map_id, layer_id)
    if current_map_layer is None:
        raise HTTPException(status_code=404, detail="Layer not found")
    current_map_layer.name = map_layer.name or current_map_layer.name
    current_map_layer.description = map_layer.description or current_map_layer.description
    current_map_layer.image = map_layer.image or current_map_layer.image

    db.commit()
    db.refresh(current_map_layer)

    return current_map_layer


def get_map_points(db: Session, map_id: int, map_layer_id: int) -> list[models.InteractiveMapPoint]:
    return db.query(models.InteractiveMapPoint).filter(models.InteractiveMapPoint.map_layer_id == map_layer_id).all()


def register_user(db: Session, discord_user_id: int, display_name: str) -> models.InteractiveMapUser:
    user = models.InteractiveMapUser(discord_id=discord_user_id, display_name=display_name)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def create_map(db: Session,
               map: schemas.MapCreate,
               author: models.InteractiveMapUser) -> models.InteractiveMap:
    db_map = models.InteractiveMap(**map.dict(),
                                   author=author.id)

    db.add(db_map)
    db.commit()
    db.refresh(db_map)

    return db_map


def get_user_display_name(db: Session,
                          user_id: int) -> str:
    return db.query(models.InteractiveMapUser).filter(models.InteractiveMapUser.id == user_id).first().display_name


def get_user_groups(db: Session,
                    user_roles: typing.List[int]):
    roles_tuple = tuple(user_roles)
    return db.query(models.InteractiveMapGroup).filter(
        models.InteractiveMapGroup.discord_group_id.in_(roles_tuple)).all()


def get_group(db: Session,
              discord_group_id: int) -> models.InteractiveMapGroup:
    groups = db.query(models.InteractiveMapGroup).filter(
        models.InteractiveMapGroup.discord_group_id == discord_group_id).all()
    if len(groups) == 0:
        return None
    return groups[0]


def get_group_by_id(db: Session,
                    id: int):
    groups = db.query(models.InteractiveMapGroup).filter(models.InteractiveMapGroup.id == id).all()
    if len(groups) == 0:
        return None
    return groups[0]


def create_group(db: Session,
                 group: schemas.MapGroupCreate):
    db_group = models.InteractiveMapGroup(**group.dict())

    db.add(db_group)
    db.commit()
    db.refresh(db_group)


def update_group(db: Session,
                 group: schemas.MapGroupCreate,
                 group_id: int):
    db_group = get_group_by_id(db, group_id)

    db_group.display_name = group.display_name or db_group.display_name

    db.commit()
    db.refresh(db_group)

    return db_group


def delete_map(db: Session,
               map_id: int):
    map = get_map(db, map_id)
    db.delete(map)
    db.commit()
