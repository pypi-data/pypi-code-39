"""
Created by 復讐者 on 2/15/19
"""
__author__ = '復讐者'


def make_campus_search_url(campus):
    campus_search_url = "https://www.coursehero.com/ajax/autocomplete_resultset.php?term=%s&type=school"
    return campus_search_url % campus

def make_course_search_url(query, csu_id):
    course_search_url = "https://www.coursehero.com/api/v1/courses/search/?q=%s&schoolId=%s"
    return course_search_url % (query, csu_id)


if __name__ == '__main__':
    pass