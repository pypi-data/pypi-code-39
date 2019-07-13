

class MetadataLoader:
    """
    Supported metadata file types
    """
    def __init__(self, configuration=None):
        from .albumart import AlbumArt

        self.configuration = configuration
        self.loaders = (
            AlbumArt,
        )

    def find_metadata_type_for_extension(self, extension):
        """
        Return metadata filetypes that match specified extension

        May return multiple
        """
        return [loader for loader in self.loaders if extension in loader(configuration=self.configuration).extensions]
