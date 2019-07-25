from IPython.display import display, HTML
from pandas import DataFrame


def patch_pandas():
    def show(self, *args, **kwargs):
        display(HTML(self.to_html(*args, **kwargs)))

    DataFrame.show = show

    
def patch():
    patch_pandas()
