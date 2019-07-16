from passlib.context import CryptContext
import psycopg2
import getpass
import signal
import sys

"""
Changes the password for the given user so long as Odoo has had a chance to encrypt and 
move it over. If it is a newly installed db, then the users password is stored in plaintext.
This script does it best to choose.
"""

dbname = "bluestingray"
dbuser = "pbuller"
dbpass = "tachyon"
dbhost = "localhost"
usertoupdate = "admin"
newpass = "admin"
newpass_crypt = CryptContext(["pbkdf2_sha512"]).encrypt(newpass)

cs = "dbname='" + dbname + "' user='" + dbuser + "' host='" + dbhost
cs = cs + "' password='" + dbpass + "'"
conn = psycopg2.connect(cs)
cur = conn.cursor()
try:
    cur.execute("UPDATE res_users SET password_crypt='" + newpass_crypt + "' where login='admin'")
except:
    cur.execute("UPDATE res_users SET password='" + newpass + "' where login='admin'")
conn.commit()
