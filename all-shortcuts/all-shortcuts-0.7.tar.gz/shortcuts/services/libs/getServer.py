def getServer(servername):
    from ...Models import Organizations,Services,Keys
    try:
        server=Organizations.select(
                Organizations,Services,Keys
            ).join(
                Services,
                on=(Organizations.id==Services.organization)
            ).join(
                Keys,
                on=(Services.key==Keys.id)
            ).where(
                (Organizations.name==servername) 
                | (Organizations.alias==servername)
            ).get()
        return server
    except:
        return False
