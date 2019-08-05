import pytz
from django.utils.dateparse import parse_datetime


def get_datetime(value, target_timezone):
    naive = parse_datetime(value)
    return pytz.timezone(target_timezone).localize(naive, is_dst=None)
