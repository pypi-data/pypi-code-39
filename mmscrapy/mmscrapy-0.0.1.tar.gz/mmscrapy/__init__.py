class Demo(object):

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def play(cls, *args, **kwargs):
        demo = cls(args, kwargs)
        return demo


if __name__ == "__main__":
    print Demo.play()
