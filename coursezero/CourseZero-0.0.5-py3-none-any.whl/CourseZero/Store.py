"""
Created by 復讐者 on 2/15/19
"""
__author__ = '復讐者'


class DataStore( object ):
    professor_first_name = None
    professor_last_name = None
    campus_name = None
    campus_id = None
    departments = [ ]
    course_ids = []

    @classmethod
    def _parse_event( cls, event ):
        if event[ 'type' ] == 'change' and event[ 'name' ] == 'value':
            v = event[ 'new' ]
            return v

    @classmethod
    def set_professor_lname( cls, event ):
        v = cls._parse_event( event )
        if v is not None:
            cls.professor_last_name = v

    @classmethod
    def set_professor_fname( cls, event ):
        v = cls._parse_event( event )
        if v is not None:
            cls.professor_first_name = v

    @classmethod
    def set_campus_name( cls, event ):
        v = cls._parse_event( event )
        if v is not None:
            cls.campus_name = v

    @classmethod
    def add_course( cls, course ):
        cls.course_ids.append( course )
        cls.course_ids = list(set(cls.course_ids))
        # cls.departments = list( set( cls.departments.append( dept ) ) )

    @classmethod
    def remove_course( cls, course ):
        el = list(filter(lambda x: x == course, cls.course_ids))[0]
        idx = cls.course_ids.index(el)
        return cls.course_ids.pop(idx)

    @classmethod
    def add_department( cls, dept ):
        cls.departments.append( dept )
        # cls.departments = list( set( cls.departments.append( dept ) ) )

    @classmethod
    def remove_department( cls, dept ):
        el = list(filter(lambda x: x == dept, cls.departments))[0]
        idx = cls.departments.index(el)
        return cls.departments.pop(idx)


class TakedownStore( DataStore ):
    agreed_w_reqd_statements = False

    @classmethod
    def toggle_statement_agreement( cls ):
        cls.agreed_w_reqd_statements = not cls.agreed_w_reqd_statements


if __name__ == '__main__':
    pass
