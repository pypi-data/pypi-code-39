from unittest import TestCase
from restclients_core.exceptions import DataFailureException
from uw_trumba.calendars import Calendars, _is_valid_calendarid


class TestCalendars(TestCase):

    def test_load(self):
        cals = Calendars().campus_calendars
        self.assertEquals(len(cals), 3)
        self.assertEquals(len(cals['bot']), 4)
        self.assertEquals(len(cals['sea']), 10)
        self.assertEquals(len(cals['tac']), 1)

        sorted_cals = sorted(cals['sea'].values())
        self.assertEqual(sorted_cals[0].name, "Seattle calendar")
        self.assertEqual(sorted_cals[1].name,
                         "Seattle calendar >> Seattle child calendar1")

        trumba_cal = cals['sea'].get(1)
        self.assertEqual(trumba_cal.calendarid, 1)
        self.assertEqual(trumba_cal.campus, 'sea')
        self.assertEqual(trumba_cal.name, 'Seattle calendar')
        perms = trumba_cal.permissions
        self.assertEqual(len(perms), 3)
        perm = perms[0]
        self.assertEqual(perm.to_json(),
                         {'level': 'PUBLISH', 'name': 'Dummy publisher',
                          'uwnetid': 'dummyp'})

        trumba_cal1 = cals['sea'].get(11321)
        print(trumba_cal1.name)
        self.assertEqual(trumba_cal1.name,
                         "{}{}{}{}".format('Seattle calendar >> Seattle',
                                           ' child calendar3 >> Seattle',
                                           ' child-sub-calendar32 >> Seattle',
                                           ' child-sub-sub-calendar321'))

    def test_is_valid_calendarid(self):
        self.assertTrue(_is_valid_calendarid(1))
        self.assertFalse(_is_valid_calendarid(0))
        self.assertFalse(_is_valid_calendarid(-1))
