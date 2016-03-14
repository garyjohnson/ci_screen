from datetime import datetime


def get_holiday_widget_path():
    today = datetime.today()
    if today.month == 4 and today.day == 1:
        return 'widgets/Weird.qml'
    if today.month == 2 and today.day in range(9,15):
        return 'widgets/Hearts.qml'
    if today.month in [1, 2, 12]:
        return 'widgets/Snow.qml'

    return None
