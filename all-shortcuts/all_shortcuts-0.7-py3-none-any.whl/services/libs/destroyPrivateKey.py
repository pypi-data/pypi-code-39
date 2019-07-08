def destroyPrivateKey(pathKey):
    import os
    from random import randrange
    for k in range(35):
        data=''
        for i in range(54):
            for i in range(64):
                data+=str(randrange(0,9))
                data+=str(randrange(0,9))
            data+="\n"
        file = open(pathKey,"w") 
        file.write(data)
        file.close() 
        os.remove(pathKey)
    return True

