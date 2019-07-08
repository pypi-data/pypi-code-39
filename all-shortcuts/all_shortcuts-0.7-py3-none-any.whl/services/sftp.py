def sftp(servername,origin,destiny,sense):
    import threading 
    from .libs import getServer
    from .libs import makePrivateKey
    from .libs import destroyPrivateKey
    from subprocess import call
    import os
    import time
    try:
        server=getServer.getServer(servername);
        if server:
            host=server.services.host
            username=server.services.username
            password=server.services.password
            port=server.services.port
            pathKey=makePrivateKey.makePrivateKey(server)
            if sense=='send':
                params=["scp", "-i", pathKey, "-P", port, origin, username+"@"+host+":"+destiny]
            elif sense=='get':
                params=["scp", "-i", pathKey, "-P", port, username+"@"+host+":"+origin, destiny]
            sftp=threading.Thread(target=call, args=(params,))
            sftp.start()
            time.sleep(3)
            destroyPrivateKey.destroyPrivateKey(pathKey)
        else:
            print ("Server not found")
    except:
        if pathKey:
            destroyPrivateKey.destroyPrivateKey(pathKey)
