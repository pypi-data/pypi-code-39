from unittest import TestCase
from uw_trumba.models import (
    is_bot, is_sea, is_tac, is_valid_campus_code, TrumbaCalendar,
    is_editor, is_showon, Permission)


class TestModels(TestCase):

    def test_is_campus(self):
        self.assertFalse(is_bot(None))
        self.assertFalse(is_bot('sea'))
        self.assertFalse(is_sea(None))
        self.assertFalse(is_sea('tac'))
        self.assertFalse(is_tac(None))
        self.assertFalse(is_tac('bot'))
        self.assertFalse(is_valid_campus_code(None))
        self.assertTrue(is_valid_campus_code('sea'))
        self.assertTrue(is_valid_campus_code('tac'))
        self.assertTrue(is_valid_campus_code('bot'))

    def test_trumba_calendar(self):
        cal = TrumbaCalendar(calendarid=1,
                             campus='sea',
                             name='CampusEvents')
        self.assertTrue(cal.is_sea())
        self.assertFalse(cal.is_bot())
        self.assertFalse(cal.is_tac())
        self.assertEqual(cal.to_json(), {'calendarid': 1,
                                         'name': 'CampusEvents',
                                         'campus': 'sea',
                                         'permissions': []})
        self.assertIsNotNone(str(cal))
        self.assertEqual(cal.get_group_admin(), "u_eventcal_support")
        self.assertIsNotNone(cal.get_group_desc('editor'))
        self.assertIsNotNone(cal.get_group_desc('showon'))
        self.assertEqual(cal.get_group_name('editor'),
                         "u_eventcal_sea_1-editor")
        self.assertEqual(cal.get_group_name('showon'),
                         "u_eventcal_sea_1-showon")
        self.assertEqual(cal.get_group_title('editor'),
                         "CampusEvents calendar editor group")
        self.assertEqual(cal.get_group_title('showon'),
                         "CampusEvents calendar showon group")
        cal2 = TrumbaCalendar(calendarid=2,
                              campus='sea',
                              name='CasEvents')
        self.assertFalse(cal == cal2)
        self.assertTrue(cal.__lt__(cal2))

    def test_is_group(self):
        self.assertTrue(is_editor('editor'))
        self.assertTrue(is_showon('showon'))

    def test_permission(self):
        self.assertEqual(len(Permission.LEVEL_CHOICES), 6)
        cal = TrumbaCalendar(calendarid=1,
                             campus='sea',
                             name='CampusEvents')
        editor = Permission(calendar=cal,
                            uwnetid='aaa',
                            level='EDIT')
        self.assertEqual(editor.get_calendarid(), 1)
        self.assertEqual(editor.get_campus_code(), 'sea')
        self.assertEqual(editor.get_trumba_userid(), "aaa@washington.edu")
        self.assertTrue(editor.is_edit())
        self.assertFalse(editor.is_showon())
        self.assertFalse(editor.is_publish())
        self.assertFalse(editor.is_republish())
        self.assertFalse(editor.is_view())
        self.assertTrue(editor.is_higher_permission('SHOWON'))
        self.assertTrue(editor.is_higher_permission('REPUBLISH'))
        self.assertTrue(editor.is_higher_permission('VIEW'))
        self.assertFalse(editor.is_higher_permission('PUBLISH'))
        self.assertTrue(editor.in_editor_group())
        self.assertFalse(editor.in_showon_group())
        self.assertFalse(editor.is_bot())
        self.assertFalse(editor.is_tac())
        self.assertTrue(editor.is_sea())
        self.assertEqual(editor.to_json(), {'level': 'EDIT',
                                            'name': None,
                                            'uwnetid': 'aaa'})
        self.assertIsNotNone(str(editor))
        self.assertTrue(editor == editor)
        cal.add_permission(editor)
        self.assertEqual(cal.to_json(),
                         {'calendarid': 1,
                          'campus': 'sea',
                          'name': 'CampusEvents',
                          'permissions': [{'level': 'EDIT',
                                           'name': None,
                                           'uwnetid': 'aaa'}]})
        perm = Permission(calendar=cal,
                          uwnetid='aaa',
                          level='SHOWON')
        self.assertTrue(perm.is_higher_permission('VIEW'))
        self.assertTrue(perm.in_showon_group())
        self.assertFalse(perm == editor)
