"""
Created by 復讐者 on 7/13/19
"""
from CourseZero.DataHandlingTools import get_by_course_id
from CourseZero.RequestTools import get_file_links_from_course_page

__author__ = '復讐者'

from IPython.display import display
from ipywidgets import widgets


# from CourseZero.Store import DataStore


# --------------------- Course selection
def make_selection_text( row ):
    """Creates the text displayed in the course selection button"""
    t = "{prof_name} ---- {dept_acro} {course_num} ----  {course_name} ----  {course_info}"
    return t.format( **row.to_dict() )


def make_course_b( row, data_store, callback=None ):
    """Creates a button for the course defined in the row.
    Sets a handler on the button to toggle whether the course is selected
    in the data store
    """
    layout = widgets.Layout( width='90%' )
    style = 'success' if row[ 'course_id' ] in data_store.course_ids else 'primary'
    b = widgets.Button( description=make_selection_text( row ), button_style=style, layout=layout )

    def handle( event ):
        if row[ 'course_id' ] in data_store.course_ids:
            data_store.remove_course( row[ 'course_id' ] )
            b.button_style = 'primary'
        else:
            data_store.add_course( row[ 'course_id' ] )
            b.button_style = 'success'

        if callback is not None:
            callback( data_store )

    b.on_click( handle )
    return b


# -------------------- Department selection

def make_dept_b( dept, data_store, callback=None ):
    style = 'success' if dept in data_store.selected_departments else 'primary'
    b = widgets.Button( description=dept, button_style=style )

    def handle( event ):
        # dept = data_store._parse_event(event)
        if dept in data_store.selected_departments:
            data_store.remove_department( dept )
            b.button_style = 'primary'
        else:
            data_store.add_department( dept )
            b.button_style = 'success'

        if callback is not None:
            callback( data_store )

    b.on_click( handle )
    return b


def split_list( a_list ):
    half = len( a_list ) // 2
    return a_list[ :half ], a_list[ half: ]


def dept_selection( data_store, callback=None ):
    """Create and display the buttons for selecting which departments
    to query"""
    buttons = [ ]
    for dept in data_store.departments:
        buttons.append( make_dept_b( dept, data_store, callback ) )

    b1, b3 = split_list( buttons )
    b1, b2 = split_list( b1 )
    b3, b4 = split_list( b3 )

    buttons = widgets.HBox( [ widgets.VBox( b1 ), widgets.VBox( b2 ), widgets.VBox( b3 ), widgets.VBox( b4 ) ] )
    label = widgets.HTML( value="<h1>Select departments to search</h1>" )
    display( widgets.VBox( [ label, buttons ] ) )


# -------------------- File selection
def make_link( url ):
    return "<a href='{}' target='_blank'>{}</a>".format( url, url )


def make_infringement_b( doc, store, callback=None ):
    """Creates a button for the document.
    Sets a handler on the button to toggle whether the doc is selected
    in the data store
    """
    layout = widgets.Layout()
    b = widgets.Button( description='NOT Infringing', button_style='primary', layout=layout )

    def handle( event ):
        if doc in store.infringing_docs:
            store.remove_doc( doc )
            b.button_style = 'primary'
            b.description = 'NOT Infringing'
        else:
            store.add_doc( doc )
            b.button_style = 'success'
            b.description = 'Infringing'

        if callback is not None:
            callback( store )

    b.on_click( handle )
    return b


# --------------------- Displaying selected file urls
def make_html_url_list( url_list ):
    """Creates a html list, enclosed in <ul> tags, of the infringing urls.
     Does not format as links to facilitate copy/pasting"""
    temp = "<li>{}</li>"
    u = "<ul>"
    for url in url_list:
        u += temp.format( url )
    u += '</ul>'
    return u


def make_infringing_table( infringing_tuples ):
    """Returns an HTML table of the infringing doc names and urls"""

    def make_row( infringing_tuple ):
        return "<tr><td>{}</td><td>{}</td></tr>".format( infringing_tuple[ 1 ], infringing_tuple[ 2 ] )

    t = "<table>"
    for infringing_tuple in infringing_tuples:
        t += make_row( infringing_tuple )
    t += "</table>"
    return t


def make_infringing_lists( infringing_tuples ):
    """Returns a copyable list infringing doc names and urls"""
    t1 = ""
    t2 = ""
    for infringing_tuple in infringing_tuples:
        t1 += "{}<br/>".format( infringing_tuple[ 1 ] )
        t2 += "{}<br/>".format( infringing_tuple[ 2 ] )
    return """
    <div class='infringing-docs'>
    <h3>Document names (as named by the uploader)</h3>
    <p>{}</p>
    <h3> Document urls</h3>
    <p>{}</p>
    </div>
    """.format( t1, t2 )


# def get_urls( frame, data_store ):
#     """Handles displaying the urls and information that has been retrieved"""
#     selected = get_by_course_id( frame, data_store.course_ids )
#     for i, r in selected.iterrows():
#         files = get_file_links_from_course_page( r[ 'url' ] )
#     return files


def show_selected_urls( frame, data_store ):
    """Handles displaying the urls and information that has been retrieved"""
    selected = get_by_course_id( frame, data_store.course_ids )
    for i, r in selected.iterrows():
        files = get_file_links_from_course_page( r[ 'url' ] )
        t = "{prof_name} ---- {dept_acro} {course_num} ----  {course_name} ----  {course_info}"
        print( t.format( **r.to_dict() ) )
        for f in files:
            print( f )


if __name__ == '__main__':
    pass
