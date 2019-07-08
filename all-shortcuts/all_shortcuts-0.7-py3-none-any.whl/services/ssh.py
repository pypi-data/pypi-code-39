def ssh(servername,byobu=True):
    import threading 
    from .libs import getServer
    from .libs import makePrivateKey
    from .libs import destroyPrivateKey
    from subprocess import call
    import time
    try:
        server=getServer.getServer(servername);
        if server:
            host=server.services.host
            username=server.services.username
            password=server.services.password
            port=server.services.port
            pathKey=makePrivateKey.makePrivateKey(server)
            ssh_connect=[
                "ssh", username+"@"+host, 
                "-p", port,
                "-i", pathKey, 
                ]
            if byobu:
                ssh_connect.append("-t")
                ssh_connect.append("byobu")
            ssh=threading.Thread(target=call, args=(ssh_connect,))
            ssh.start()
            time.sleep(3)
            destroyPrivateKey.destroyPrivateKey(pathKey)
        else:
            print ("Server not found")
    except:
        if pathKey:
            destroyPrivateKey.destroyPrivateKey(pathKey)
