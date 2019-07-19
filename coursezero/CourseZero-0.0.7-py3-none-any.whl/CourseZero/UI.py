"""
Created by 復讐者 on 7/18/19
"""
__author__ = '復讐者'

import datetime

from IPython.display import display
from ipywidgets import widgets

import environment as env
from CourseZero.DataHandlingTools import parse_json_into_df
from CourseZero.Errors import UnsetValue
from CourseZero.RequestTools import get_docs_for_campus
from CourseZero.Store import TakedownStore
from CourseZero.Widgets.Inputs import dept_selection
from CourseZero.Widgets.Inputs import make_course_b
from CourseZero.Widgets.Inputs import make_link, make_infringement_b, make_infringing_lists
from CourseZero.Widgets.TakedownInputs import make_text_input, make_email_helper_button


# from CourseZero.Store import DataStore


def show_email_draft_area():
    field_map = { r[ 'prop' ]: make_text_input( r ) for r in TakedownStore.input_fields }
    inputs = list( field_map.values() )

    def make_email_draft( **kwargs ):
        letter_date = datetime.date.isoformat( datetime.date.today() )
        #         doc_urls = make_html_url_list(TakedownStore.data_store.infringing_docs)
        doc_urls = make_infringing_lists( TakedownStore.data_store.infringing_doc_tuples )
        with open( '{}/takedown_request.html'.format( env.TEMPLATE_FOLDER ), 'r' ) as o:
            template = o.read()

        formatted = template.format( letter_date=letter_date, doc_urls=doc_urls, **kwargs )
        return display( widgets.HTML( value=formatted ) )

    # Show the email draft and fields to fill it in
    email_out = widgets.interactive_output( make_email_draft, field_map )
    return display( widgets.VBox( [ widgets.VBox( inputs ), email_out ] ) )


def search_depts( data_store ):
    """Callback which queries the site for departments associated with the selected
    campus. It then fires a callback which drills down to courses in the department,
    and so on.
    """
    try:

        # dev !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        # Query for results and parse them into a dataframe
        json_data = get_docs_for_campus( data_store.campus_id, data_store.campus_name )
        data_store.data = parse_json_into_df( json_data )

        print( "{} courses identified at {}".format( len( data_store.data ), data_store.campus_name ) )
        print( "{} department names located".format( len( data_store.departments ) ) )

        # Create the output areas
        progress_out = widgets.Output( layout={ 'border': '1px solid black' } )
        display( progress_out )
        depts_out = widgets.Output( layout={ 'border': '1px solid black' } )
        display( depts_out )
        courses_out = widgets.Output( layout={ 'border': '1px solid black' } )
        display( courses_out )
        docs_out = widgets.Output( layout={ 'border': '1px solid black' } )
        display( docs_out )
        takedown_out = widgets.Output( layout={ 'border': '1px solid black' } )
        display( takedown_out )
        email_out = widgets.Output( layout={ 'border': '1px solid black' } )
        display( email_out )

        # make the store accessible on the TakedownStore class
        # this is a shortcut for getting the store inside callbacks
        TakedownStore.data_store = data_store

        def search_courses( data_store ):
            """Make buttons for courses corresponding to the selected departments"""
            course_buttons = [ ]
            for i, r in data_store.selected_departments_data.iterrows():
                course_buttons.append( make_course_b( r, data_store, search_documents ) )

            buttons = widgets.VBox( course_buttons )
            label = widgets.HTML( value="<h1>Select courses to search</h1>" )
            courses_out.clear_output()
            with courses_out:
                display( widgets.VBox( [ label, buttons ] ) )

        def search_documents( data_store ):
            """Displays selection buttons for the documents associated with the selected courses"""
            rows = [ widgets.HBox(
                [ make_infringement_b( d, data_store, show_takedown ), widgets.HTML( value=make_link( d ) ) ] ) for d in
                     data_store.selected_courses_documents_urls ]
            docs_out.clear_output()
            with open( '{}/file_selection_instructions.html'.format( env.TEMPLATE_FOLDER ), 'r' ) as o:
                doc_instructions = o.read()

            doc_instructions = widgets.HTML( value=doc_instructions )
            with docs_out:
                display( widgets.VBox( [ doc_instructions, widgets.VBox( rows ) ] ) )

        def show_takedown( data_store ):
            """Callback which controls whether the information about submitting a takedown request
            is displayed"""
            if len( data_store.infringing_docs ) == 0: pass

            with open( '{}/takedown_instructions.html'.format( env.TEMPLATE_FOLDER ), 'r' ) as o:
                takedown_instructions = o.read()
                # add list of urls
                #                 url_list = make_infringing_table(data_store.infringing_doc_tuples)
                url_list = make_infringing_lists( data_store.infringing_doc_tuples )
                #                 url_list = make_html_url_list(data_store.infringing_docs)
                format_args = { 'url_list': url_list }
                takedown_instructions = takedown_instructions.format( **format_args )
                takedown_instructions = widgets.HTML( value=takedown_instructions )

            takedown_out.clear_output()

            with takedown_out:
                display( widgets.VBox( [ takedown_instructions, make_email_helper_button( show_email_draft_area ) ] ) )

        # Show the department selection
        # buttons and other output areas
        with depts_out:
            dept_selection( data_store, search_courses )

    except UnsetValue as e:
        print( e.message )


if __name__ == '__main__':
    pass
