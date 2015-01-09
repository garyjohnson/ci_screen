from datetime import datetime


def get_holiday_widget_path():
    if datetime.today().month in [1, 2, 12]:
        return 'widgets/Snow.qml'

    return None
