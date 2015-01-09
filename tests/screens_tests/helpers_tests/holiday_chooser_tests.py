import unittest

from freezegun import freeze_time

import screens.helpers.holiday_chooser as holiday_chooser


class HolidayChooserTests(unittest.TestCase):

    @freeze_time('2013-05-01')
    def test_no_widget_by_default(self):
        actual_path = holiday_chooser.get_holiday_widget_path()

        self.assertIsNone(actual_path)

    @freeze_time('2015-12-01')
    def test_snow_appears_at_start_of_december(self):
        actual_path = holiday_chooser.get_holiday_widget_path()

        self.assertEquals('widgets/Snow.qml', actual_path)
    
    @freeze_time('2015-02-28')
    def test_snow_appears_at_end_of_february(self):
        actual_path = holiday_chooser.get_holiday_widget_path()

        self.assertEquals('widgets/Snow.qml', actual_path)

    
        
        

