"""
Created by 復讐者 on 7/13/19
"""
from unittest import TestCase

from CourseZero.Errors import UnsetValue
from CourseZero.Store import DataStore
__author__ = '復讐者'

if __name__ == '__main__':
    pass


class TestDataStore( TestCase ):
    def test__parse_event( self ):
        self.fail()

    def test_set_professor_fname( self ):
        self.fail()

    def test_professor_first_name( self ):
        self.fail()

    def test_set_professor_lname( self ):
        self.fail()

    def test_professor_last_name( self ):
        self.fail()

    def test_set_campus_name( self ):
        self.fail()

    def test_campus_name( self ):
        d = DataStore(None)
        d.campus_name = 'taco'
        self.assertEqual(d.campus_name, 'taco')


    def test_campus_id_getter( self ):
        tv = 35
        DataStore.campus_id = tv
        self.assertEqual(DataStore.campus_id, tv)

    def test_campus_id_getter_raises_when_empty( self ):
        # self.assertIs(p, None)
        with self.assertRaises(UnsetValue):
            p = DataStore.campus_id

    def test_campus_id( self ):
        self.fail()

    def test_add_course( self ):
        self.fail()

    def test_remove_course( self ):
        self.fail()

    def test_add_department( self ):
        self.fail()

    def test_remove_department( self ):
        self.fail()
