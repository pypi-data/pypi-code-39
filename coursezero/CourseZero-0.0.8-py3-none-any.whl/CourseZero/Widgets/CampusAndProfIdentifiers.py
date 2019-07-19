"""
Created by 復讐者 on 2/15/19
"""
__author__ = '復讐者'


"""
Created by 復讐者 on 1/7/19
"""
__author__ = '復讐者'

from IPython.display import display
from ipywidgets import widgets

# from CourseZero.Store import DataStore

# -------- General
def make_text_input( input_dict ):
    """Creates a text input field. The given dictionary should have keys 'label' and 'handler'"""
    text = widgets.Text( description=input_dict[ 'label' ] )
    display( text )
    text.observe( input_dict[ 'handler' ] )
    return text


def make_campus_selector( store, callback=None ):
    csu_names = [c['name'] for c in store.campus_ids ]
    layout = widgets.Layout( width='80%' )
    campus_sel = widgets.Dropdown(
        options=csu_names,
        description='Campus',
        disabled=False,
        layout=layout,
        )
    campus_ids = store.campus_ids

    def campus_select_handler(event):
        if event[ 'type' ] == 'change' and event[ 'name' ] == 'value':
            v = event['new']
            # set the campus name
            store.campus_name = v
            # look up the id and store it
            cid = list(filter(lambda x: x['name'] == v, campus_ids))
            store.campus_id = cid[0 ][ 'campus_id' ]

            if callback is not None:
                callback(store)

    campus_sel.observe( campus_select_handler )

    label = widgets.HTML(value="<h1>Select campus to search</h1>")
    display(widgets.VBox([label, campus_sel]))


if __name__ == '__main__':
    pass