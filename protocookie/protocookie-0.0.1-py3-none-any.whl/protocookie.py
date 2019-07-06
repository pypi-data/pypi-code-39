#!/usr/bin/env python
"""
Example usage:
    import protocookie
    protocookie.encryptionKey = <encryption key>
    encrypted = encrypt(_userDefinition)
    decrypted = decrypt(encrypted))

with open("./data.json", "r") as fd:
    data = json.load(fd)
"""

from . import protocookie_pb2 as pcookie
import json
from cryptography.fernet import Fernet

encryptionKey = None

def _defineService(obj):
    attrMap = {
            "OWNER"  : pcookie.Service.Role.OWNER,
            "VIEWER" : pcookie.Service.Role.VIEWER,
            "EDITOR" : pcookie.Service.Role.EDITOR,
        }

    service = pcookie.Service()
    service.serviceName = obj["name"]
    service.serviceID = obj["id"]
    list(map(
        service.roles.append,
        list(map(
            attrMap.get,
            obj["perm"]
        ))
    ))

    return service

def _defineUser(obj):
    user = pcookie.User()
    user.username = obj["username"]
    user.id = obj["id"]
    list(map(
        user.services.append, list(map(
            _defineService,
            obj["services"]
            ))
    ))

    return user

def encrypt(obj):
    pbObj = _defineUser(obj)
    cipher_suite = Fernet(encryptionKey)
    return cipher_suite.encrypt(pbObj.SerializeToString())

def decrypt(data):
    cipher_suite = Fernet(encryptionKey)
    return pcookie.User.FromString(cipher_suite.decrypt(data))

