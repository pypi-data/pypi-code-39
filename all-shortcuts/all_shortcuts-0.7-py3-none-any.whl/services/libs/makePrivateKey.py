def makePrivateKey(server):
    import base64
    from random import randrange
    import os
    privateKey=str(
            base64.b64decode(
                server.services.keys.private
                )
            ).replace(
                    '\\n',
                    "\n"
                    )[2:-2]
    keyName=str(randrange(10000,99999))
    pathKey='/tmp/'+keyName
    file = open(pathKey,"w") 
    file.write(privateKey)
    file.close() 
    os.chmod(pathKey,0o600)
    return pathKey

