import unittest

from freezegun import freeze_time

import ci_screen.screens.helpers.holiday_chooser as holiday_chooser


class HolidayChooserTests(unittest.TestCase):

    @freeze_time('2017-05-01')
    def test_no_widget_by_default(self):
        actual_path = holiday_chooser.get_holiday_widget_path()

        self.assertIsNone(actual_path)

    @freeze_time('2100-12-01')
    def test_snow_appears_at_start_of_december(self):
        actual_path = holiday_chooser.get_holiday_widget_path()

        self.assertEquals('widgets/Snow.qml', actual_path)
    
    @freeze_time('2012-02-28')
    def test_snow_appears_at_end_of_february(self):
        actual_path = holiday_chooser.get_holiday_widget_path()

        self.assertEquals('widgets/Snow.qml', actual_path)

    @freeze_time('2020-02-09')
    def test_hearts_appear_five_days_before_valentines_day(self):
        actual_path = holiday_chooser.get_holiday_widget_path()

        self.assertEquals('widgets/Hearts.qml', actual_path)

    @freeze_time('2018-02-14')
    def test_hearts_appear_on_valentines_day(self):
        actual_path = holiday_chooser.get_holiday_widget_path()

        self.assertEquals('widgets/Hearts.qml', actual_path)

    @freeze_time('2016-02-15')
    def test_hearts_do_not_appear_after_valentines_day(self):
        actual_path = holiday_chooser.get_holiday_widget_path()

        self.assertNotEquals('widgets/Hearts.qml', actual_path)

    @freeze_time('2013-03-31')
    def test_weird_stuff_does_not_appear_before_april_fools(self):
        actual_path = holiday_chooser.get_holiday_widget_path()

        self.assertNotEquals('widgets/Weird.qml', actual_path)

    @freeze_time('2013-04-01')
    def test_weird_stuff_appears_on_april_fools(self):
        actual_path = holiday_chooser.get_holiday_widget_path()

        self.assertEquals('widgets/Weird.qml', actual_path)

    @freeze_time('2013-04-02')
    def test_weird_stuff_does_not_appear_after_april_fools(self):
        actual_path = holiday_chooser.get_holiday_widget_path()

        self.assertNotEquals('widgets/Weird.qml', actual_path)
