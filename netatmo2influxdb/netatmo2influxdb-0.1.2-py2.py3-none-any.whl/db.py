import sqlite3
from datetime import datetime

DB_FILE = "netatmo.db"


def init_db(clear_db=False):
    """
    Initialize database. The clear_db argument allows for a clean start.
    """
    if clear_db:
        sql_clear_users = """ DROP TABLE IF EXISTS users; """
        sql_clear_records = """ DROP TABLE IF EXISTS records; """
        _execute(sql_clear_users)
        _execute(sql_clear_records)
    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                            username text PRIMARY KEY,
                            refresh_token text,
                            access_token text,
                            expires_ts int
                        ); """
    sql_create_records_table = """ CREATE TABLE IF NOT EXISTS records (
                            username text,
                            home_id text,
                            room_id text,
                            start_ts int,
                            end_ts int,
                            count int,
                            created_ts int
                        );"""
    _execute(sql_create_users_table)
    _execute(sql_create_records_table)


def _create_connection():
    """
    Create a sqlite3 connection object
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        return conn
    except Exception as e:
        print(e)

    return None


def _execute(sql: str):
    """
    Execute SQL
    """
    conn = _create_connection()
    try:
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)


def _dict_factory(cursor, row):
    """
    Creates a dict with row-names as keys for every query.
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def create_user(username: str, refresh_token: str, access_token: str, expires_ts: int):
    """
    Create a user
    """
    conn = _create_connection()
    sql = f""" INSERT INTO users(username, refresh_token, access_token, expires_ts)
              VALUES(\'{username}\',
                    \'{refresh_token}\',
                    \'{access_token}\',
                    {expires_ts}) """
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()


def update_user(username: str, access_token: str, expires_ts: int):
    """
    Update a user access token and expiration timestamp.
    """
    conn = _create_connection()
    sql = f""" UPDATE users SET
                access_token = '{access_token}',
                expires_ts = {expires_ts}
                WHERE username = '{username}'"""
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()


def get_user(username: str):
    """
    Retrieve a user by username (username, refresh_token, access_token, expires_ts)
    """
    conn = _create_connection()
    conn.row_factory = _dict_factory
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE username='{username}'")
    user = cur.fetchone()
    return user


def create_record(
    username: str, home_id: str, room_id: str, start_ts: int, end_ts: int, count: int
):
    """
    Create a record of import query
    """
    created_ts = datetime.utcnow().timestamp()
    conn = _create_connection()
    sql = f""" INSERT INTO records(username, home_id, room_id,
                                   start_ts, end_ts, count, created_ts)
            VALUES(
                \'{username}\',
                \'{home_id}\',
                \'{room_id}\',
                {start_ts},
                {end_ts},
                {count},
                {created_ts}) """
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()


def get_last_record(username, home_id, room_id):
    """
    Get last record by username, home, and room.
    """
    conn = _create_connection()
    conn.row_factory = _dict_factory
    cur = conn.cursor()
    sql = f""" SELECT * FROM records
            WHERE username = \'{username}\' AND
                home_id=\'{home_id}\' AND
                room_id=\'{room_id}\' AND
                created_ts=(SELECT MAX(created_ts)
            FROM records WHERE username=\'{username}\' AND
                            home_id=\'{home_id}\' AND
                            room_id=\'{room_id}\')"""
    cur.execute(sql)
    record = cur.fetchone()
    return record
