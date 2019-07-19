"""
Created by 復讐者 on 2/15/19
"""
from CourseZero.Store import TakedownStore

__author__ = '復讐者'

from IPython.display import display
from ipywidgets import widgets
from time import sleep


def make_email_helper_button( callback=None ):
    """Creates a button for the document.
    Sets a handler on the button to toggle whether the doc is selected
    in the data store
    """
    layout = widgets.Layout( width='30%' )

    b = widgets.Button( description='Create draft takedown email', button_style='info', layout=layout )

    def handle( event ):
        if callback is not None:
            callback()

    b.on_click( handle )
    return b


def make_text_input( input_dict ):
    """Creates a text input field. The given dictionary should have keys 'label' and 'handler'"""
    style = { 'description_width': 'initial' }
    text = widgets.Text( description=input_dict[ 'label' ], name=input_dict[ 'prop' ], style=style )
    # display( text )
    text.observe( TakedownStore.event_handler )
    return text




def progress_bar( output_area, label='Searching' ):
    """Creates an indefinitely repeating progress bar
    which keeps running until something calls output_area.clear_output()
    DOES NOT WORK PROPERLY
    """
    stop = 100
    i = 0

    progress = widgets.IntProgress(
        value=0,
        min=0,
        max=stop,
        description=label,
        bar_style='info',
        orientation='horizontal'
    )

    with output_area:
        display( progress )
    while True:
        if i > stop:
            i = 0
        sleep( .1 )
        i += 1
        progress.value = i


if __name__ == '__main__':
    pass
