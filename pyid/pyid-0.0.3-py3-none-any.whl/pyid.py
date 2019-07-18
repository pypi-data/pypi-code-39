import uuid


def idfy(obj, id=None):
    if not id:
        id = uuid.uuid4()
    superclass = obj.__class__
    classname = superclass.__name__
    id_class = type(
        classname,
        (superclass,),
        {
            'id': id,
        }
    )
    id_obj = id_class(obj)
    return id_obj
