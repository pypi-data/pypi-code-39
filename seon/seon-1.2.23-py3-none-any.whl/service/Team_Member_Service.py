from .Service_Abstract import Service_Abstract

class Team_Member_Service(Service_Abstract):

    def __init__(self):
        Service_Abstract.__init__(self,'teammembers')