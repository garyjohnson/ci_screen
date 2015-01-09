from datetime import datetime


def get_holiday_widget_path():
    today = datetime.today()
    if today.month == 2 and today.day == 9:
        return 'widgets/Hearts.qml'
    if today.month in [1, 2, 12]:
        return 'widgets/Snow.qml'

    return None
