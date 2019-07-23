class DTO(object):
    def __init__(self, cls):                                                                                                                      
    
        def frozensetattr(self, key, value):                                                                                                   
            if not hasattr(self, key):                                                                 
                raise AttributeError("Class {} is frozen. Cannot set {} = {}"                                                                                 
                      .format(cls.__name__, key, value))                                                                                       
            else:                                                                                                                              
                self.__dict__[key] = value                                                                                                     
    
        cls.__setattr__ = frozensetattr 
        self.cls = cls
        
    def __call__(self, *args, **kwargs):
        return self.cls(*args, **kwargs)