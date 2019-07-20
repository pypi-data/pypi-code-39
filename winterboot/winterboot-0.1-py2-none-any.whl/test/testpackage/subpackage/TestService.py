from winterboot.Service import Service
@Service
class TestService(object):
    def canBeCalled(self):
        return True