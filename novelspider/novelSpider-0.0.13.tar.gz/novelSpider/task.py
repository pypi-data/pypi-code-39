from app.novelDownloader import novelDownloader

class Task(object):
    __version__ = '0.0.13'
    def createDownloader(self, Config):
        config = Config()
        downloader = novelDownloader(config)
        return downloader
