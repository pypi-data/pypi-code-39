class default():
    """
    Default conifguration
    """
    DEBUG=False
    TESTING=False
    LOGLEVEL='INFO'
    ENVIRONMENT='default'
    EMAIL='resif-dc@univ-grenoble-alpes.fr'

    GNUPGHOMEDIR='../../tests/test_files/gpg_home'

    AUTHDBPORT=5432
    AUTHDBHOST='localhost'
    AUTHDBNAME='resifAuth'
    AUTHDBUSER='eidawsauth'
    AUTHDBPASSWORD='secret'

    PRIVILEGEDBHOST='localhost'
    PRIVILEGEDBPORT=5432
    PRIVILEGEDBNAME='resifInv-Prod'
    PRIVILEGEDBUSER='eidawsauth'
    PRIVILEGEDBPASSWORD='secret'

    EPOS_FDSN_MAP={
        '/epos/alparray': {'networkcode':'Z3', 'startyear':2015, 'endyear': 2020},
    }
