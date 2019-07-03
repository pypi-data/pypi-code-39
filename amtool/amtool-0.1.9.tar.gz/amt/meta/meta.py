__all__ = ['MetaDict', 'MetaList']


class MetaDict(dict):
    """
    Dictionary with metadata.

    This object is used to store dictionaries in an object tree with metadata
    about source.  An example is if an artifact tree is loaded from a heirarchy
    of files, then then relative path information of source files will be
    stored in the metadata.
    """
    pass


class MetaList(list):
    """
    List with metadata.

    This object is used to store lists in an object tree with metadata about
    source.  An example is if an artifact tree is loaded from a heirarchy of
    files, then then relative path information of source files will be stored
    in the metadata.
    """
    pass
