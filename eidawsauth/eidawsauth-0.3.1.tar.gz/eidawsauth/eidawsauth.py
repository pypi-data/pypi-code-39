import gnupg
import re
import datetime
import random
import string
import logging
import os
from hashlib import md5
from flask import Flask, request, Response
import configurations
import psycopg2
from version import __version__
from psycopg2.extensions import AsIs

application = Flask(__name__)
if 'RUNMODE' in os.environ and os.environ['RUNMODE'] == 'production':
    application.config.from_object(configurations.production.config)
elif 'RUNMODE' in os.environ and os.environ['RUNMODE'] == 'development':
    application.config.from_object(configurations.development.config)
else:
    application.config.from_object(configurations.default.default)

from logging.config import dictConfig
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': application.config['LOGLEVEL'],
        'handlers': ['wsgi']
    }
})

def wsshash(login, password):
    """
    Compute a hash suitable for the IRIS wss stack.
    """
    return md5(("%s:FDSN:%s"%(login,password)).encode()).hexdigest()

def verify_token_signature(data, gpg_homedir):
    # First we verify the signature
    gpg = gnupg.GPG(gnupghome=gpg_homedir)
    verified = gpg.verify(data)
    if not verified: raise ValueError("Signature could not be verified!")
    return True

def parse_input_data(data):
    # Then we get the token :
    token = re.search(r'{(?P<token>.*)}',str(data)).groupdict()['token']
    logging.debug(token)
    d = dict([i for i in kv.split(':',1)] for kv in token.replace('"','').replace(' ','').split(','))

    logging.debug("Transformed to dictionary : "+str(d))
    return d

def register_login(login, password):
    """
    - Connects to the AUTHDB
    - Generate Login and Password hash
    - register in the users table
    """
    try:
        conn = psycopg2.connect(dbname= application.config['AUTHDBNAME'],
                            port = application.config['AUTHDBPORT'],
                            host = application.config['AUTHDBHOST'],
                            user= application.config['AUTHDBUSER'],
                            password = application.config['AUTHDBPASSWORD'])
        cur = conn.cursor()
        logging.debug("Connected to users database")
    except Exception as e:
        logging.error("Unable to connect to database %s as %s@%s:%s"%(application.config['AUTHDBNAME'],
                                                                      application.config['AUTHDBUSER'],
                                                                      application.config['AUTHDBHOST'],
                                                                      application.config['AUTHDBPORT']))
        raise e

    cur.execute("""
                INSERT INTO users VALUES (DEFAULT, %(login)s, 'Temp', 'EIDA', %(tmpmail)s, %(expiration)s);
                """,
                {'login': login, 'tmpmail': "%s@eida"%(login),'expiration': datetime.datetime.now()+datetime.timedelta(days=1)}
    )

    cur.execute("""
        INSERT INTO credentials VALUES (CURRVAL('users_user_index_seq'), NULL, %(wsshash)s);
        """,
                {'wsshash': wsshash(login, password)}
    )
    conn.commit()
    conn.close()

def register_privileges(login, fdsn_refs):
    """
    - Connect to PRIVILEGEDB
    - For each fdsn reference, insert the privilege in the access table
    """
    try:
        conn = psycopg2.connect(dbname= application.config['PRIVILEGEDBNAME'],
                            port = application.config['PRIVILEGEDBPORT'],
                            host = application.config['PRIVILEGEDBHOST'],
                            user= application.config['PRIVILEGEDBUSER'],
                            password = application.config['PRIVILEGEDBPASSWORD'])
        cur = conn.cursor()
        logging.debug("Connected to users database")
    except Exception as e:
        logging.error("Unable to connect to database %s as %s@%s:%s"%(application.config['PRIVILEGEDBNAME'],
                                                                      application.config['PRIVILEGEDBUSER'],
                                                                      application.config['PRIVILEGEDBHOST'],
                                                                      application.config['PRIVILEGEDBPORT']))
        raise e

    # Get the network id
    for ref in fdsn_refs:
        ref['login'] = login
        cur.execute("""
                    select network_id from networks where start_year=%(startyear)s and end_year=%(endyear)s and network=%(networkcode)s;
                    """, ref)
        ref['networkid'] = cur.fetchone()[0]
        logging.info(ref)
        cur.execute("""
                    insert into eida_temp_users (network_id, network, start_year, end_year, name) values (%(networkid)s, %(networkcode)s, %(startyear)s, %(endyear)s, %(login)s);
                    """, ref)
    conn.commit()
    conn.close()


@application.route("/version", methods=['GET'])
def version():
    return Response("Version %s running in %s mode. Contact %s."%(__version__, application.config['ENVIRONMENT'], application.config['EMAIL']), status=200)

@application.route("/cleanup", methods=['GET'])
def cleanup():
    """
    Clean old temporary logins and passwords in both databases.
    """
    try:
        conn = psycopg2.connect(dbname= application.config['AUTHDBNAME'],
                            port = application.config['AUTHDBPORT'],
                            host = application.config['AUTHDBHOST'],
                            user= application.config['AUTHDBUSER'],
                            password = application.config['AUTHDBPASSWORD'])
        cur = conn.cursor()
        logging.debug("Connected to users database")
    except Exception as e:
        logging.error("Unable to connect to database %s as %s@%s:%s"%(application.config['AUTHDBNAME'],
                                                                      application.config['AUTHDBUSER'],
                                                                      application.config['AUTHDBHOST'],
                                                                      application.config['AUTHDBPORT']))
        raise e

    cur.execute("select user_index,login from users where expires_at < now();")
    old_users_entries = cur.fetchall()[:1000]
    old_users = ','.join( str(u[0]) for u in old_users_entries )
    logging.debug("%d users to delete"%(len(old_users_entries)))
    try :
        cur.execute("delete from credentials where user_index in (%s);",(AsIs(old_users),))
        cur.execute("delete from users where user_index in (%s);", (AsIs(old_users),))
    except Exception as e:
        logging.error("Unable de delete from credentials or users")
        logging.error(e)
    conn.commit()
    conn.close()

    try:
        conn = psycopg2.connect(dbname= application.config['PRIVILEGEDBNAME'],
                            port = application.config['PRIVILEGEDBPORT'],
                            host = application.config['PRIVILEGEDBHOST'],
                            user= application.config['PRIVILEGEDBUSER'],
                            password = application.config['PRIVILEGEDBPASSWORD'])
        cur = conn.cursor()
        logging.debug("Connected to privlieges database")
    except Exception as e:
        logging.error("Unable to connect to database %s as %s@%s:%s"%(application.config['PRIVILEGEDBNAME'],
                                                                      application.config['PRIVILEGEDBUSER'],
                                                                      application.config['PRIVILEGEDBHOST'],
                                                                      application.config['PRIVILEGEDBPORT']))
        raise e
    logging.debug("Deleting from privileges database")
    old_users =  ','.join(str(u[1]) for u in old_users_entries)
    cur.execute("""
        delete from eida_temp_users where name in (%s);
        """, (old_users,))
    conn.commit()
    conn.close()
    return Response("Deleted %d temporary accounts."%(len(old_users_entries)), status=200)

@application.route("/", methods=['POST'])
def auth():
    login = ''
    password = ''
    logging.debug(request.mimetype)
    data = request.get_data()
    logging.debug("Data: %s", data)
    try:
        verify_token_signature(data, application.config['GNUPGHOMEDIR'])
        tokendict = parse_input_data(data)
        logging.info("Token signature OK: %s"%str(tokendict))
    except ValueError as e:
        logging.info("Token signature could not be checked: %s"%str(data))
        return Response(str(e), status=415)
    # Now we have a dictionary corresponding to the token's content.
    # Verify validity
    expiration_ts=  datetime.datetime.strptime(tokendict['valid_until'], '%Y-%m-%dT%H:%M:%S.%fZ')
    if (expiration_ts - datetime.datetime.now()).total_seconds() < 0:
        logging.info("Token is expired")
        return Response('Token is expired. Please generate a new one at https://geofon.gfz-potsdam.de/eas/', status=415)
    logging.info("Token is valid")

    # Check membership and get FDSN references
    fdsn_memberships = []
    for em in  tokendict['memberof'].split(';'):
        if em in application.config['EPOS_FDSN_MAP']:
            fdsn_memberships.append(application.config['EPOS_FDSN_MAP'][em])
    # If fdsn_memberships is empty, there is no point to continue.
    if len(fdsn_memberships) == 0 :
        logging.info("User has no access to any data hosted here.")
        return Response("This token does not grant access to any data hosted at RESIF. You are member of %s. Please contact the PI of the data you are looking for to grant you access."%tokendict['memberof'], status=200)

    # Compute a random login and password
    login = ''.join(random.choices(string.ascii_uppercase + string.digits, k=14))
    password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=14))

    # Register login
    register_login(login, password)

    # Store in PRIVILEGEDB
    register_privileges(login, fdsn_memberships)
    # Return
    return "%s:%s"%(login, password)

if __name__ == "__main__":
    logging.info("Running in %s mode"%(application.config['ENVIRONMENT']))
    application.run(host='0.0.0.0')
