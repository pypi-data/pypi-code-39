import getpass
import os
from datetime import datetime
from sqlite3 import IntegrityError

import requests
from logger import logger

import db

NETATMO_BASE = os.getenv("NETATMO_BASE")
# Specific to API security
CLIENT_ID = os.getenv("CLIENT_ID")
if not CLIENT_ID:
    raise EnvironmentError("Missing CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
if not CLIENT_SECRET:
    raise EnvironmentError("Missing CLIENT_SECRET")


def get_access_token(username):
    logger.debug(f"Fetching access token for {username}")
    user = db.get_user(username)
    if user is None:  # User does not exist yet, create initial tokens
        logger.debug(f"First time use for user {username} - initializing tokens")
        token = init_tokens(username)
        return token["access_token"]

    # Check if token has expired
    logger.debug(f"Checking if token expired")
    now = datetime.utcnow().timestamp()
    expires = user["expires_ts"]
    if now >= expires:
        # If the token has expired, refresh
        logger.debug(f"Token expired, getting a new token")
        token = refresh_access_token(username)
        return token["access_token"]

    # Everything is OK
    return user["access_token"]


def init_tokens(username):
    logger.debug(f"Requesting password for first time user {username}")
    # Request password in terminal
    password = getpass.getpass(prompt=f"Password for {username}: ")

    # Create request
    url = NETATMO_BASE + "oauth2/token"
    data = {
        "grant_type": "password",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "username": username,
        "password": password,
        "scope": "read_thermostat write_thermostat",
    }
    resp = requests.post(url, data=data)
    if resp.status_code != 200:
        logger.critical(f"Could not get user access tokens for user {username}")
        raise ConnectionError(f"Something went wrong: {resp.json()}")

    # Process data and save to db
    logger.debug(f"Successfully got information for user {username}")
    tkn = resp.json()
    now = datetime.utcnow().timestamp()
    expires_ts = now + tkn["expires_in"]
    try:
        logger.debug(f"Creating database entry for user {username}")
        db.create_user(username, tkn["refresh_token"], tkn["access_token"], expires_ts)
    except IntegrityError:
        logger.warning(
            f"User {username} already exists in database.\
            Only updating access_token."
        )
        db.update_user(username, tkn["access_token"], expires_ts)
    return tkn


def refresh_access_token(username):
    # Get user
    user = db.get_user(username)
    logger.debug(f"Getting refresh token for user {username}")
    refresh_token = user["refresh_token"]

    # Create request
    url = NETATMO_BASE + "oauth2/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    resp = requests.post(url, data=data)
    if resp.status_code != 200:
        logger.critical(
            f"Could not connect to the Netatmo API or\
            Refresh Token is invalid"
        )
        raise ConnectionError("Could not connect to Netatmo API")

    # Process data and save in db
    logger.debug(f"Storing new access token in database")
    tkn = resp.json()
    now = datetime.utcnow().timestamp()
    expires_ts = now + tkn["expires_in"]

    # Update user
    db.update_user(username, tkn["access_token"], expires_ts)
    return tkn
