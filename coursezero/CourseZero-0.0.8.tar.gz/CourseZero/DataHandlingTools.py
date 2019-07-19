"""
Created by 復讐者 on 7/13/19
"""
from CourseZero.RequestTools import get_file_links_from_course_page

__author__ = '復讐者'

import pandas as pd

import environment as env


def parse_counts( row ):
    """The server returns a field with a list of
    the various kinds of documents that have been uploaded.
    This parses those counts out and adds them as columns to the frame
    """
    for c in row[ 'doc_counts' ]:
        row[ c[ 'category' ] ] = c[ 'count' ]
    return row


def parse_json_into_df( json_data, fields=env.JSON_FIELDS ):
    """Parse json data into a usable dataframe
    For now: Control which columns are kept by commenting out in JSON_FIELDS
    """
    data = [ ]

    for r in json_data:
        try:
            if r[ 'total' ] > 0:
                for row in r[ 'results' ]:
                    data.append( row )

        except Exception as e:
            pass

    data = pd.DataFrame( data )
    # Filter out unneeded columns
    data = data[ fields ]
    # Add the counts of each kind of document to the frame as a column
    data = data.apply( lambda r: parse_counts( r ), axis=1 )
    # Drop the counts column so can de-dupe (list isn't hashable)
    data.drop( [ 'doc_counts' ], axis=1, inplace=True )
    data.drop_duplicates( inplace=True )
    return data


# Data frame operations
def get_departments( frame ):
    """Extract list of departments from the results frame"""
    depts = list( set( frame.dept_acro.tolist() ) )
    depts.sort()
    return depts


def normalize_prof_name( prof_name ):
    return prof_name.strip().upper()


# Frame filtration operations
def filter_by_dept_abbrevs( frame, dept_list ):
    """Uses the list of departments defined by the user to
    return those departments from the results frame"""
    return frame[ frame[ 'dept_acro' ].isin( dept_list) ]


def get_by_course_id( frame, course_ids ):
    """Finds and reeturns a course or list of courses from the results
    frame"""
    if type( course_ids ) is not list:
        course_ids = list( course_ids )
    return frame[ frame[ 'course_id' ].isin( course_ids ) ]


def get_urls( frame, course_ids ):
    """Gets the links to files which appear on the
    course pages for courses that the user has selected
     Returns a list of tuples: (course id, doc name, doc url)
     """
    files = []
    selected = get_by_course_id( frame, course_ids )
    for i, r in selected.iterrows():
        # print(r[ 'url' ])
        coursepage_url = r[ 'url' ]
        fs = get_file_links_from_course_page( coursepage_url )
        # This returned a list of tuples (doc name, doc url)
        # We'll make a new tuple with the course id as the first
        # item: (course id, doc name, doc url)
        files += [ ( r['course_id'], name, url) for name, url in fs ]
    return files


if __name__ == '__main__':
    pass
