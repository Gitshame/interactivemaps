import json
import os
import typing
import urllib
import requests

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse, Response

from jose import JWTError, jwt

from .database import SessionLocal, engine
from . import crud, models, schemas
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

ORIGINS = [i.strip() for i in os.environ.get('ORIGINS', '').split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AUTH_REDIRECT = os.environ.get('DISCORD_AUTH_REDIRECT')
CLIENT_ID = os.environ.get('DISCORD_CLIENT_ID')
CLIENT_SECRET = os.environ.get('DISCORD_CLIENT_SECRET')
BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

DISCORD_URL_BASE = "https://discord.com"
DISCORD_API_BASE = f"{DISCORD_URL_BASE}/api/v10"

OAUTH_SCOPES = ['identify']

SECRET_KEY = os.environ.get('JWT_TOKEN_SECRET')
ALGORITHM = os.environ.get('JWT_TOKEN_ALGO', "HS256")


def get_discord_token_from_code(code: str):
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': AUTH_REDIRECT
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    r = requests.post(f'{DISCORD_API_BASE}/oauth2/token', data=data, headers=headers)
    r.raise_for_status()

    return r.json()


def get_discord_user(token: typing.Dict):
    headers = {
        'Authorization': f"{token['token_type']} {token['access_token']}",
    }
    endpoint = f"{DISCORD_API_BASE}/users/@me"

    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()

    return response.json()


def generate_jwt_from_user(user: typing.Dict):
    encoded_jwt = jwt.encode(user, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_bot_guilds():
    headers = {
        'Authorization': f'Bot {BOT_TOKEN}'
    }
    endpoint = f"{DISCORD_API_BASE}/users/@me/guilds"
    api_response = requests.get(endpoint, headers=headers)

    api_response.raise_for_status()

    return api_response.json()


def get_members_from_guild(guild_id: int):
    headers = {
        'Authorization': f'Bot {BOT_TOKEN}'
    }
    params = {
        "limit": 1000
    }

    endpoint = f"{DISCORD_API_BASE}/guilds/{guild_id}/members"
    output = []

    while True:
        api_response = requests.get(endpoint, headers=headers, params=params)

        api_response.raise_for_status()

        api_json = api_response.json()
        highest_id = 0

        for user in api_json:
            output.append(user)
            user_id = int(user['user']['id'])
            if user_id > highest_id:
                highest_id = user_id

        if len(api_json) < 1000:
            break

        params['after'] = highest_id

    return output


def get_known_roles_for_user(user_id: int, bot_guilds: typing.List):
    user_roles = []

    for guild in bot_guilds:
        members = get_members_from_guild(guild['id'])

        member = [m for m in members if m['user']['id'] == user_id][0]

        user_roles.extend(member['roles'])

    return user_roles


def populate_group_objects(guild_id: int, guild_name: str):
    headers = {
        'Authorization': f'Bot {BOT_TOKEN}'
    }

    endpoint = f"{DISCORD_API_BASE}/guilds/{guild_id}/roles"
    api_response = requests.get(endpoint, headers=headers)

    api_response.raise_for_status()

    roles = api_response.json()

    db = SessionLocal()

    for role in roles:
        db_role = crud.get_group(db, role['id'])
        updated_role = schemas.MapGroupCreate(discord_group_id=role['id'],
                                              display_name=role['name'],
                                              server_name=guild_name)
        if not db_role:
            print("creating")
            db_role = crud.create_group(db, updated_role)
        else:
            print("updating")
            db_role = crud.update_group(db, updated_role, db_role.id)


@app.get('/login')
def get_login():
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'scope': ' '.join(OAUTH_SCOPES),
        'redirect_uri': AUTH_REDIRECT
    }

    redirect_url = f"{DISCORD_URL_BASE}/oauth2/authorize?{urllib.parse.urlencode(params, doseq=True)}"

    return RedirectResponse(redirect_url)


@app.get('/callback')
def get_callback(code: str):
    if not code:
        raise HTTPException(status_code=400, detail="Invalid code")

    return RedirectResponse(url=f"http://localhost:9000/?code={code}")


@app.get('/token')
def get_token(code: str):
    if not code:
        raise HTTPException(status_code=400, detail="Invalid code")

    discord_token = get_discord_token_from_code(code)

    user = get_discord_user(discord_token)
    guilds = get_bot_guilds()

    roles = get_known_roles_for_user(user['id'], bot_guilds=guilds)

    jwt_contents = {
        "discord": user,
        "discord_groups": roles,
        # TODO: Add expiration
        "expiration": "NEVERRRRRR"
    }

    for guild in guilds:
        populate_group_objects(guild['id'], guild['name'])

    return generate_jwt_from_user(jwt_contents)
