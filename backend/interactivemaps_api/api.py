import json
import os
import typing

import requests as requests
from fastapi import FastAPI, Depends, HTTPException, Header, WebSocket, WebSocketDisconnect
from .database import SessionLocal, engine
from . import crud, models, schemas
from .crud import get_db, get_user, get_groups
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from dataclasses import dataclass

models.Base.metadata.create_all(bind=engine)

ORIGINS = [i.strip() for i in os.environ.get('ORIGINS', '').split(",")]
AUTH_BASE_URL = os.environ.get("AUTH_TOKEN_URL")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependencies
@dataclass
class WebsocketConnection:
    user: schemas.UserData
    socket: WebSocket

class WebsocketConnectionManager:
    def __init__(self):
        self.active_connections: list[WebsocketConnection] = []

    async def connect(self, websocket: WebsocketConnection):
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebsocketConnection):
        self.active_connections.remove(websocket)

    async def map_notification(self, map_id: int):
        for connection in self.active_connections:
            await connection.socket.send_json({'type': 'map', 'map': map_id})

    async def layer_notification(self, map_id: int, layer_id: int):
        session = next(get_db())

        layer = crud.get_map_layer(session, map_id, layer_id)
        for connection in self.active_connections:
            db_user = crud.get_db_user(session, connection.user)
            groups = crud.get_groups(connection.user, session)
            permissions = crud.summarize_permissions(session, layer_id, db_user, layer, groups)
            if permissions.get('read'):
                await connection.socket.send_json({'type': 'layer', 'map': map_id, 'layer': layer_id})

    async def point_notification(self, map_id: int, layer_id: int, point_id: int):
        session = next(get_db())

        layer = crud.get_map_layer(session, map_id, layer_id)
        for connection in self.active_connections:
            db_user = crud.get_db_user(session, connection.user)
            groups = crud.get_groups(connection.user, session)
            permissions = crud.summarize_permissions(session, layer_id, db_user, layer, groups)
            if permissions.get('read'):
                await connection.socket.send_json({'type': 'point', 'map': map_id, 'layer': layer_id, 'point': point_id})


websocketManager = WebsocketConnectionManager()

@app.websocket('/ws')
async def route_websocket(websocket: WebSocket,
                          db: typing.Annotated[Session, Depends(get_db)]):
    await websocket.accept()

    token = await websocket.receive_text()
    user = get_user(db, f"Bearer {token}")

    if not user:
        await websocket.close(reason='Authorization failed')
        return

    ws_connection = WebsocketConnection(socket=websocket, user=user)
    await websocketManager.connect(ws_connection)
    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        websocketManager.disconnect(ws_connection)

@app.get('/token')
def route_get_token(code: str):
    resp = requests.get(f"{AUTH_BASE_URL}/token?code={code}")
    return {"token": resp.text[1:-1]}


@app.get('/login', response_class=RedirectResponse)
def route_login():
    return RedirectResponse(f"{AUTH_BASE_URL}/login")


@app.get('/me', response_model=schemas.MyUser)
def get_my_user(db_user: typing.Annotated[models.InteractiveMapUser, Depends(crud.get_db_user)]):
    return {'discord_id': db_user.discord_id,
            'display_name': db_user.display_name,
            'is_admin': db_user.admin}


@app.get('/maps', response_model=typing.List[schemas.Map])
def route_get_maps(user: typing.Annotated[typing.Optional[models.InteractiveMapUser], Depends(crud.get_user)],
                   db: typing.Annotated[Session, Depends(get_db)]):
    user_id_cache = {}

    maps = crud.get_maps(db)
    output = []

    for map in maps:
        map_data = map.__dict__
        user_id = map_data['author']
        if user_id_cache.get(user_id):
            display_name = user_id_cache.get(user_id)
        else:
            display_name = crud.get_user_display_name(db, map_data['author'])
            user_id_cache[user_id] = display_name

        map_data['author'] = display_name

        output.append(map_data)

    return output


@app.post("/maps", response_model=schemas.Map)
async def route_create_map(user: typing.Annotated[schemas.UserData, Depends(get_user)],
                     db_user: typing.Annotated[models.InteractiveMapUser, Depends(crud.get_db_user)],
                     is_admin: typing.Annotated[bool, Depends(crud.is_admin)],
                     map: schemas.MapCreate,
                     db: typing.Annotated[Session, Depends(get_db)]):
    map = crud.create_map(db, map, db_user)

    response_data = map.__dict__
    response_data['author'] = crud.get_user_display_name(db, response_data['author'])

    await websocketManager.map_notification(response_data['id'])

    return response_data


@app.patch("/maps/{map_id}", response_model=schemas.Map)
async def route_update_map(user: typing.Annotated[schemas.UserData, Depends(get_user)],
                     map_id: int,
                     map: schemas.MapUpdate,
                     is_admin: typing.Annotated[bool, Depends(crud.is_admin)],
                     db_map: typing.Annotated[models.InteractiveMap, Depends(crud.get_map)],
                     db: typing.Annotated[Session, Depends(get_db)]):
    updated_map = crud.update_map(db, map_id, map)

    response_data = updated_map.__dict__
    response_data['author'] = crud.get_user_display_name(db, response_data['author'])

    await websocketManager.map_notification(map_id)

    return response_data


@app.get("/maps/{map_id}", response_model=schemas.MapDetails)
async def route_get_map_details(user: typing.Annotated[schemas.UserData, Depends(get_user)],
                          db_user: typing.Annotated[models.InteractiveMapUser, Depends(crud.get_db_user)],
                          map_id: int,
                          map: typing.Annotated[models.InteractiveMap, Depends(crud.get_map)],
                          db_map: typing.Annotated[models.InteractiveMap, Depends(crud.get_map)],
                          groups: typing.Annotated[typing.List[models.InteractiveMapGroup], Depends(get_groups)],
                          db: typing.Annotated[Session, Depends(get_db)]):
    all_layers = crud.get_layers(db, map_id)
    output_layers = []
    for layer in all_layers:
        if user:
            permissions = crud.summarize_permissions(db, layer.id, db_user, layer, groups)
            if permissions['read']:
                new_layer = layer.__dict__
                new_layer['permissions'] = permissions
                output_layers.append(new_layer)

    response_data = map.__dict__
    response_data['layers'] = output_layers

    return response_data


@app.delete("/maps/{map_id}")
async def route_delete_map(user: typing.Annotated[schemas.UserData, Depends(get_user)],
                     map_id: int,
                     is_admin: typing.Annotated[bool, Depends(crud.is_admin)],
                     db_map: typing.Annotated[models.InteractiveMap, Depends(crud.get_map)],
                     db: typing.Annotated[Session, Depends(get_db)]):
    crud.delete_map(db, map_id)

    await websocketManager.map_notification(map_id)
    return


@app.post("/maps/{map_id}/layers", response_model=schemas.MapLayerSummary)
async def route_create_layer(user: typing.Annotated[schemas.UserData, Depends(get_user)],
                       db_user: typing.Annotated[models.InteractiveMapUser, Depends(crud.get_db_user)],
                       map_id: int,
                       layer: schemas.MapLayerCreate,
                       groups: typing.Annotated[typing.List[models.InteractiveMapGroup], Depends(get_groups)],
                       db: typing.Annotated[Session, Depends(get_db)]):
    if layer.public:
        crud.is_admin(db_user)

    new_layer = crud.create_map_layer(db, map_id, layer, db_user.id)

    user_perm_entry = schemas.LayerUserPermissionEntry(user_id=db_user.id,
                                                       read=True,
                                                       create=True,
                                                       modify=True,
                                                       delete=True)

    new_permissions = schemas.LayerPermissionSummary(user_permissions=[user_perm_entry], group_permissions=[])

    crud.set_layer_permissions(db, new_layer.id, new_permissions)
    db.refresh(new_layer)

    layer_data = new_layer.__dict__
    layer_data['author'] = crud.get_user_display_name(db, layer_data['author'])
    layer_data['permissions'] = crud.summarize_permissions(db, new_layer.id, db_user, new_layer, groups)

    await websocketManager.layer_notification(map_id, layer_data['id'])

    return layer_data


@app.get("/maps/{map_id}/layers/{layer_id}", response_model=schemas.MapLayerDetails)
def route_get_layer_details(layer_id: int,
                            db_user: typing.Annotated[models.InteractiveMapUser, Depends(crud.get_db_user)],
                            layer: typing.Annotated[models.InteractiveMapLayer, Depends(crud.get_map_layer)],
                            map: typing.Annotated[models.InteractiveMap, Depends(crud.get_map)],
                            groups: typing.Annotated[typing.List[models.InteractiveMapGroup], Depends(get_groups)],
                            has_read: typing.Annotated[bool, Depends(crud.has_layer_read_permission)],
                            permissions: typing.Annotated[typing.Dict, Depends(crud.summarize_permissions)],
                            db: typing.Annotated[Session, Depends(get_db)]):
    response = layer.__dict__

    response['points'] = crud.get_map_points(db, map.id, layer.id)
    response['permissions'] = permissions

    return response


@app.patch("/maps/{map_id}/layers/{layer_id}", response_model=schemas.MapLayer)
async def route_update_layer(map_id: int,
                       layer_id: int,
                       layer: schemas.MapLayerUpdate,
                       db: typing.Annotated[Session, Depends(get_db)],
                       db_layer: typing.Annotated[models.InteractiveMapLayer, Depends(crud.get_map_layer)],
                       has_modify: typing.Annotated[bool, Depends(crud.has_layer_modify_permission)]):
    layer_data = crud.update_map_layer(db, map_id, layer_id, layer).__dict__
    layer_data['author'] = crud.get_user_display_name(db, layer_data['author'])

    await websocketManager.layer_notification(map_id, layer_data['id'])

    return layer_data

@app.delete("/maps/{map_id}/layers/{layer_id}")
def route_delete_layer(map_id: int,
                       layer_id: int,
                       db: typing.Annotated[Session, Depends(get_db)],
                       has_delete: typing.Annotated[bool, Depends(crud.has_layer_delete_permission)]):
    crud.delete_layer(db, map_id, layer_id)
    websocketManager.layer_notification(map_id, layer_id)


@app.post("/maps/{map_id}/layers/{layer_id}/points", response_model=schemas.MapPoint)
async def route_create_point(map_id: int,
                       layer_id: int,
                       point: schemas.MapPointCreate,
                       db_user: typing.Annotated[models.InteractiveMapUser, Depends(crud.get_db_user)],
                       db: typing.Annotated[Session, Depends(get_db)],
                       db_layer: typing.Annotated[models.InteractiveMapLayer, Depends(crud.get_map_layer)],
                       has_create: typing.Annotated[bool, Depends(crud.has_layer_create_permission)]):
    new_point = crud.create_map_point(db, db_layer, point, db_user)

    await websocketManager.point_notification(map_id, layer_id, new_point.id)

    return new_point

@app.patch("/maps/{map_id}/layers/{layer_id}/points/{point_id}", response_model=schemas.MapPoint)
def route_update_point(map_id: int,
                       layer_id: int,
                       point_id: int,
                       point: schemas.MapPointUpdate,
                       db_user: typing.Annotated[models.InteractiveMapUser, Depends(crud.get_db_user)],
                       db: typing.Annotated[Session, Depends(get_db)],
                       db_layer: typing.Annotated[models.InteractiveMapLayer, Depends(crud.get_map_layer)],
                       has_modify: typing.Annotated[bool, Depends(crud.has_layer_modify_permission)]):
    return crud.update_point(db, point_id, point)

@app.delete("/maps/{map_id}/layers/{layer_id}/points/{point_id}")
async def route_delete_point(map_id: int,
                       layer_id: int,
                       point_id: int,
                       db: typing.Annotated[Session, Depends(get_db)],
                       has_delete: typing.Annotated[bool, Depends(crud.has_layer_delete_permission)]):
    await websocketManager.point_notification(map_id, layer_id, point_id)

    crud.delete_point(db, point_id)

@app.get("/maps/{map_id}/layers/{layer_id}/permissions", response_model=schemas.LayerPermissionSummary)
def route_get_permissions(map_id: int,
                          layer_id: int,
                          db: typing.Annotated[Session, Depends(get_db)]):
    return {'user_permissions': crud.get_all_user_layer_permissions(db, layer_id),
            'group_permissions': crud.get_all_group_layer_permissions(db, layer_id)}
@app.get("/users", response_model=schemas.UsersList)
def route_get_users(
        db: typing.Annotated[Session, Depends(get_db)],
        db_user: typing.Annotated[models.InteractiveMapUser, Depends(crud.get_db_user)]):
    if not db_user:
        raise HTTPException(status_code=401, detail='Unauthorized')

    users = crud.get_all_users(db)

    return {"users": [schemas.UserSummary(id=i.id, display_name=i.display_name) for i in users]}

@app.get("/groups", response_model=schemas.GroupsList)
def route_get_groups(
        db: typing.Annotated[Session, Depends(get_db)],
        db_user: typing.Annotated[models.InteractiveMapUser, Depends(crud.get_db_user)]):
    if not db_user:
        raise HTTPException(status_code=401, detail='Unauthorized')

    groups = crud.get_all_groups(db)

    return {"groups": [schemas.GroupSummary(id=g.id, display_name=g.display_name, server_name=g.server_name) for g in groups]}

@app.post("/maps/{map_id}/layers/{layer_id}/permissions", response_model=schemas.LayerPermissionSummary)
async def route_post_permissions(map_id: int,
                           layer_id: int,
                           db: typing.Annotated[Session, Depends(get_db)],
                           new_permissions: schemas.LayerPermissionSummary,
                           has_modify: typing.Annotated[bool, Depends(crud.has_layer_modify_permission)]):
    crud.set_layer_permissions(db, layer_id, new_permissions)

    await websocketManager.layer_notification(map_id, layer_id)

    return route_get_permissions(map_id,
                                 layer_id,
                                 db)