import datetime


def get_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def format_issue(issue):
    mapping = {
        'Leakage': 'Leakage',
        'Water leakage': 'Water leakage',
        'No Water': 'No Water',
        'No water': 'No water',
        'Dirty Water': 'Dirty Water',
        'Dirty water': 'Dirty water',
        'Low Pressure': 'Low Pressure',
        'Low pressure': 'Low pressure',
    }
    return mapping.get(issue, issue)


def is_valid_phone(phone):
    return phone.isdigit() and len(phone) >= 10
