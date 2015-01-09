from datetime import datetime


def get_holiday_widget_path():
    if datetime.today() == datetime(2015, 12, 01):
        return 'widgets/Snow.qml'

    return None
