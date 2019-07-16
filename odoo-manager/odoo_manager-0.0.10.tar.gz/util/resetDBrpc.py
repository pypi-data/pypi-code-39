"""
Resets the expiration date of an odoo instance using RPC.

Change five items:
 1. the path variable, pointing the instance of odoo you wish to update.
 2. dbname - database name
 3. username
 4. password
 5. new_date - what the date should be set too

"""
import xmlrpclib

dbname = "Client_Bluestingray_V10"
username = "admin"
password = "mv7rd1ts"

new_date = "2017-03-27 18:00:00"

path = "http://bci.odoods.com:80/xmlrpc/2"
common = xmlrpclib.ServerProxy(path + "/common")
uid = common.authenticate(dbname, username, password, {})
models = xmlrpclib.ServerProxy(path + "/object")
parameters = models.execute_kw(
    dbname, uid, username, "ir.config_parameter", "search_read", [], {"fields": ["id", "key", "value"]}
)

print("BEFORE:")
for p in parameters:
    print(p)
pid = [p["id"] for p in parameters if p["key"] == "database.expiration_date"][0]

parameters = models.execute_kw(dbname, uid, username, "ir.config_parameter", "write", [[pid], {"value": new_date}])
parameters = models.execute_kw(
    dbname, uid, username, "ir.config_parameter", "search_read", [], {"fields": ["id", "key", "value"]}
)

print("AFTER:")
for p in parameters:
    print(p)
