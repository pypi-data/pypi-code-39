"""
Created by 復讐者 on 2/15/19
"""

__author__ = '復讐者'

from CourseZero.DataHandlingTools import get_by_course_id, get_urls

# from CourseZero.DataHandlingTools import get_departments
# from CourseZero.DataStorageTools import load_campus_id_data

from CourseZero.Errors import UnsetValue


# class classproperty(object):
#
#     def __init__(self, fget):
#         self.fget = fget
#
#     def __get__(self, owner_self, owner_cls):
#         return self.fget(owner_cls)

def warn_if_empty( func ):
    """When class properties are retrieved, this
    checks whether they are empty and raises an exception if so"""

    def func_wrapper( *args, **kwargs ):
        result = func( *args, **kwargs )
        if result is None or len( result ) == 0:
            raise UnsetValue( func.__name__ )
        return result

    return func_wrapper


def prop_inspector_dec( func ):
    """When class properties are retrieved, this
    checks whether they are empty and raises an exception if so"""

    def func_wrapper( *args, **kwargs ):
        print( func.__name__ )
        cls_prop_name = "_{}".format( func.__name__ )
        if getattr( args[ 0 ], cls_prop_name ) is None:
            raise UnsetValue( func.__name__ )
        return func( *args, **kwargs )

    return func_wrapper


class DStore( object ):
    _professor_first_name = None
    _professor_last_name = None
    campus_name = None
    campus_id = None
    departments = [ ]
    course_ids = [ ]

    @classmethod
    def _parse_event( cls, event ):
        if event[ 'type' ] == 'change' and event[ 'name' ] == 'value':
            v = event[ 'new' ]
            return v

    @classmethod
    def set_professor_fname( cls, event ):
        v = cls._parse_event( event )
        if v is not None:
            cls._professor_first_name = v

    @property
    @prop_inspector_dec
    def professor_first_name( cls ):
        return cls._professor_first_name

    @classmethod
    def set_professor_lname( cls, event ):
        v = cls._parse_event( event )
        if v is not None:
            cls._professor_last_name = v

    @property
    @prop_inspector_dec
    def professor_last_name( cls ):
        return cls._professor_last_name

    @classmethod
    def set_campus_name( cls, event ):
        v = cls._parse_event( event )
        if v is not None:
            cls.campus_name = v

    # @property
    # @prop_inspector_dec
    # def campus_name( cls ):
    #     return cls._campus_name

    # @prop_inspector_dec
    # @property
    # def campus_id( cls ):
    #     return cls._campus_id
    #
    # @campus_id.setter
    # def campus_id( cls, campus_id ):
    #     cls._campus_id = campus_id

    @classmethod
    def add_course( cls, course ):
        cls.course_ids.append( course )
        cls.course_ids = list( set( cls.course_ids ) )
        # cls.departments = list( set( cls.departments.append( dept ) ) )

    @classmethod
    def remove_course( cls, course ):
        el = list( filter( lambda x: x == course, cls.course_ids ) )[ 0 ]
        idx = cls.course_ids.index( el )
        return cls.course_ids.pop( idx )

    @classmethod
    def add_department( cls, dept ):
        cls.departments.append( dept )
        # cls.departments = list( set( cls.departments.append( dept ) ) )

    @classmethod
    def remove_department( cls, dept ):
        el = list( filter( lambda x: x == dept, cls.departments ) )[ 0 ]
        idx = cls.departments.index( el )
        return cls.departments.pop( idx )


class DataStore( object ):

    def __init__( self ):
        self.data = None
        """DataFrame with query results """

        self.campus_ids = [ ]
        """"""

        self.campus_name = None
        """The name of the campus that we are searching"""

        self.campus_id = None
        """The id of the campus that we are searching"""

        self.course_ids = [ ]
        """The ids of courses in which the user wants to search for infinging docs"""

        self.selected_departments = [ ]
        """Departments selected by the user for searching"""

        self._selected_course_documents = []

        self.infringing_docs = [ ]
        """Document urls which the user has selected as infringing"""

    @property
    def csu_names( self ):
        return [ c[ 'name' ] for c in self.campus_ids ]

    @property
    def departments( self ):
        """All departments for the campus  from the results frame"""
        depts = list( set( self.data.dept_acro.tolist() ) )
        depts.sort()
        return depts

    def _parse_event( self, event ):
        if event[ 'type' ] == 'change' and event[ 'name' ] == 'value':
            v = event[ 'new' ]
            return v

    def add_course( self, course ):
        self.course_ids.append( course )
        self.course_ids = list( set( self.course_ids ) )
        # cls.departments = list( set( cls.departments.append( dept ) ) )

    def remove_course( self, course ):
        el = list( filter( lambda x: x == course, self.course_ids ) )[ 0 ]
        idx = self.course_ids.index( el )
        return self.course_ids.pop( idx )

    def add_department( self, dept ):
        """Adds a department to the list of departments the user wants to view"""
        self.selected_departments.append( dept )
        # cls.departments = list( set( cls.departments.append( dept ) ) )

    def remove_department( self, dept ):
        """Removes a department from the list of departments that the user wants to view"""
        el = list( filter( lambda x: x == dept, self.selected_departments ) )[ 0 ]
        idx = self.selected_departments.index( el )
        return self.selected_departments.pop( idx )

    @property
    def selected_departments_data( self ):
        """Uses the list of departments selected by the user to
        return those departments from the results frame
        returns DataFrame
        """
        return self.data[ self.data[ 'dept_acro' ].isin( self.selected_departments ) ]

    @property
    def selected_courses_documents( self ):
        """Returns dataframe with the documents """
        return get_by_course_id( self.data, self.course_ids )

    def _get_docs_for_selected_courses( self ):
        """This will populate _selected_course_documents with tuples
        of the form: (course id, doc name, doc url)
        Since we want to minimize queries to the site, it will only fire
        if the list is empty or there's been a change in selected courses.
        In the latter case, it will retrieve any new courses and remove any
        that are no longer selected
        """
        # If we haven't yet checked the server for documents, we do so
        if len(self._selected_course_documents) == 0:
            self._selected_course_documents = get_urls( self.data, self.course_ids )
        else:
            # remove any documents for courses that have been de-selected
            self._selected_course_documents = list( filter( lambda x: x[ 0 ] in self.course_ids, self._selected_course_documents ) )

            # get documents where courses have been added
            existing = list(set([ cid for cid, name, url in self._selected_course_documents]))
            added = [ cid for cid in self.course_ids if cid not in existing ]
            if len(added) > 0:
                self._selected_course_documents += get_urls( self.data, added )


    @property
    def selected_courses_documents_urls( self ):
        """Returns a list of the file urls by querying the course pages
         and harvesting all urls pointing at a file"""
        self._get_docs_for_selected_courses()
        return [ url for cid, name, url in self._selected_course_documents]

        # for i, r in self.selected_courses_documents.iterrows():
        #     files = get_file_links_from_course_page( r[ 'url' ] )
        # return files

    @property
    def selected_courses_documents_names( self ):
        """Returns a list of the names of the files from the selected courses
        """
        self._get_docs_for_selected_courses()
        return [ name for cid, name, url in self._selected_course_documents]

    @property
    def infringing_doc_names( self ):
        return [name for cid, name, url in self.infringing_doc_tuples]

    @property
    def infringing_doc_tuples( self ):
        return [t for t in self._selected_course_documents if t[2] in self.infringing_docs]

    def add_doc( self, url ):
        """Add a file url to the list of allegedly infringing documents"""
        self.infringing_docs.append( url )

    def remove_doc( self, url ):
        """Remove a file url from the list of allegedly infringing documents"""
        idx = self.infringing_docs.index( url )
        return self.infringing_docs.pop( idx )


class TakedownStore( object ):
    """Stores data for creating takedown request letter"""
    name = None
    address = None
    email = None
    data_store = None

    input_fields = [
        { 'label': 'Your full name', 'prop': 'prof_name' },
        { 'label': 'Your institution', 'prop': 'institution' },
        { 'label': 'Department', 'prop': 'department' },
        { 'label': 'Street address', 'prop': 'street_address' },
        { 'label': 'City', 'prop': 'city' },
        { 'label': 'State', 'prop': 'state' },
        { 'label': 'Zipcode', 'prop': 'zip' },
        { 'label': 'Email address', 'prop': 'email' },
        #  {'label':'', 'prop': ''}
    ]

    # @property
    # def infringing_docs( self ):
    #
    @classmethod
    def event_handler( cls, event ):
        if event[ 'type' ] == 'change' and event[ 'name' ] == 'value':
            v = event[ 'new' ]
            # lookup the property from the label
            label = getattr( event[ 'owner' ], 'description' )
            update_prop = list( filter( lambda x: x[ 'label' ] == label, cls.input_fields ) )[ 0 ][ 'prop' ]
            setattr( cls, update_prop, v )

    # @classmethod
    # def add_doc( cls, url ):
    #     cls.infringing_docs.append( url )
    #
    # @classmethod
    # def remove_doc( cls, url ):
    #     idx = cls.infringing_docs.index( url )
    #     return cls.infringing_docs.pop( idx )

    # @property
    # def is_ready( cls ):
    #     return None not in [cls.name, cls.email, cls.address]

    # @property
    # def doc_urls( cls, infringing_docs ):
    #     """Creates a html list of the infringing urls without
    #     them formatted as links to facilitate copy/pasting"""
    #     temp = "<li>{}</li>"
    #     u = "<ul>"
    #     for url in infringing_docs:
    #         u += temp.format( url )
    #     u += '</ul>'
    #     return u
    #
    # @classmethod
    # def format_args( cls, infringing_docs ):
    #     return {
    #         'letter_date': datetime.date.isoformat( datetime.date.today() ),
    #         'name': cls.name,
    #         'email': cls.email,
    #         'address': cls.address,
    #         'doc_urls': infringing_docs
    #     }


if __name__ == '__main__':
    pass
