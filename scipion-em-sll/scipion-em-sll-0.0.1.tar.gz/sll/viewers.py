


class ImageBox(Item):
    def __init__(self, canvas, imgPath, x=0, y=0, text=None):
        Item.__init__(self, canvas, x, y)
        # Create the image
        from pyworkflow.gui import getImage, getImageFromPath

        if imgPath is None:
            self.image = getImage('no-image.png')
        else:
            self.image = getImageFromPath(imgPath)

        if text is not None:
            self.label = tk.Label(canvas, image=self.image, text=text,
                                  compound=tk.TOP, bg='gray')
            self.id = self.canvas.create_window(x, y, window=self.label)
            self.label.bind('<Button-1>', self._onClick)
        else:
            self.id = self.canvas.create_image(x, y, image=self.image)

    def setSelected(self, value):  # Ignore selection highlight
        pass

    def _onClick(self, e=None):
        pass