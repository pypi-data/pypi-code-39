from IPython.display import display, HTML
from pandas import DataFrame
from .styler import Styler


def patch_pandas():
    def show(self, *args, **kwargs):
        display(HTML(self.to_html(*args, **kwargs)))

    DataFrame.show = show
    
def patch_styler():
    def style(self):
        return Styler(self)

    setattr(DataFrame, 'style', property(style))

    
def patch():
    patch_pandas()
    patch_styler()
