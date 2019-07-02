from abconfig.common import Dict


class Attrs(Dict):
    """ Class attribute parser.

    Reads all public attributes of the class
    that was passed as an argument.
    """

    def __init__(self, obj: Dict):
        super().__init__({
            str(x): getattr(obj, x)
            for x in type(obj).__dict__.keys()
            if (x[:2] != '__' and x[:1] != '_')
        })


class Finalize(Dict):
    """ The final step of abconfig processing.

    Replaces type objects remaining after processing with None,
    a neutral element for Item monoid.
    """

    def __init__(self, x: Dict):
        super().__init__(
            x.fmap(lambda i:
                (i[0], Finalize(i[1]))
                if isinstance(i[1], (dict, Dict)) else
                (i[0], None if isinstance(i[1], type) else i[1])
            )
        )
