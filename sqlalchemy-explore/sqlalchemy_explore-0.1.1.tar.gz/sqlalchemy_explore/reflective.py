from typing import List, Dict

class ReflectiveMixin:
    @staticmethod
    def sa_key_from_column(column_name):
        return column_name[column_name.rfind('.') +1:]
    
    def sa_keys(self) -> List[str]:
        """
        returns the list of attribute names that are mapped to SQLAlchemy columns
        """
        return [
            ReflectiveMixin.sa_key_from_column(str(col)) 
            for col in 
            self.__table__.columns
            ]
    
    def sa_dict(self) -> Dict[str, object]:
        """
        returns a dictionary mapping of keys to their values
        """
        return {key: getattr(self, key) for key in self.sa_keys()}
    
    def __repr__(self) -> str:
        return "{}({})".format(
            type(self).__name__,
            ', '.join(["{}={!r}".format(name, value) for name, value in self.sa_dict().items()])
        )

def reflective(class_):
    """
    decorator for SQLAlchemy Base in case you don't want to inherit from ReflectiveMixin
    """
    class_.sa_keys = ReflectiveMixin.sa_keys
    class_.sa_dict = ReflectiveMixin.sa_dict
    class_.__repr__ = ReflectiveMixin.__repr__
    return class_
