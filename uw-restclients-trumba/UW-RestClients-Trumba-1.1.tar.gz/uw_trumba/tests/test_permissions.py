from unittest import TestCase
from restclients_core.exceptions import DataFailureException
from uw_trumba.models import TrumbaCalendar
from uw_trumba.permissions import (
    get_cal_permissions, _create_get_perm_body, _check_err,
    _extract_uwnetid, _is_valid_email)
from uw_trumba.exceptions import (
    TrumbaException, CalendarNotExist, CalendarOwnByDiffAccount,
    NoDataReturned, UnknownError, UnexpectedError)


class TestPermissions(TestCase):

    def test_get_cal_permissions(self):
        cal = TrumbaCalendar(calendarid=1,
                             campus='sea',
                             name='Seattle calendar')
        get_cal_permissions(cal)
        perms = cal.permissions
        self.assertEqual(len(perms), 3)
        self.assertTrue(perms[0].is_higher_permission(perms[1].level))
        self.assertTrue(perms[1].is_higher_permission(perms[2].level))

    def test_check_err(self):
        self.assertRaises(UnexpectedError,
                          _check_err,
                          {"d": {"Messages": [{"Code": 3009,
                                               "Description": "..."}]}})

        self.assertRaises(CalendarOwnByDiffAccount,
                          _check_err,
                          {"d": {"Messages": [{"Code": 3007}]}})

        self.assertRaises(CalendarNotExist,
                          _check_err,
                          {"d": {"Messages": [{"Code": 3006}]}})

        self.assertRaises(NoDataReturned,
                          _check_err, {'d': None})

        self.assertRaises(UnknownError,
                          _check_err,
                          {"d": {"Messages": []}})

        self.assertRaises(UnknownError,
                          _check_err,
                          {"d": {"Messages": [{"Code": None}]}})

        self.assertIsNone(_check_err({"d": {"Messages": None}}))

    def test_create_body(self):
        self.assertEqual(_create_get_perm_body(1),
                         '{"CalendarID": 1}')

    def test_is_valid_email(self):
        self.assertTrue(_is_valid_email('test@washington.edu'))
        self.assertTrue(_is_valid_email('test-email@washington.edu'))
        self.assertTrue(_is_valid_email('test_email@washington.edu'))
        self.assertTrue(_is_valid_email('test.email@washington.edu'))
        self.assertFalse(_is_valid_email('test@uw.edu'))
        self.assertFalse(_is_valid_email('0test@washington.edu'))
        self.assertFalse(_is_valid_email(''))

    def test_extract_uwnetid(self):
        self.assertEqual(_extract_uwnetid('test@washington.edu'), 'test')
        self.assertEqual(_extract_uwnetid('test'), 'test')
        self.assertEqual(_extract_uwnetid('@washington.edu'), '')
        self.assertEqual(_extract_uwnetid('bad@uw.edu'), 'bad@uw.edu')
        self.assertEqual(_extract_uwnetid(''), '')
