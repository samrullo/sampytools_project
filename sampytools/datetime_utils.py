import pandas as pd
import numpy as np
import datetime
import logging

def to_str():
    return datetime.datetime.strftime

def to_yyyymmdd(date):
    return to_str(date, '%Y%m%d')


def to_yyyymmdd_with_hyphen(date):
    return to_str(date, '%Y-%m-%d')


def to_mmddyyyy_with_slash(date):
    return to_str(date, '%m/%d/%Y')


def ppd_price_risk_date_strptime(strdate, date_pattern='%m/%d/%y'):
    return datetime.datetime.strptime(strdate, date_pattern)


def get_day_of_week(adate):
    """
    Get weekday based on datetime.date
    :param adate:
    :return:
    """
    weekdays = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"}
    return weekdays[adate.weekday()]


def get_npdatetime64_business_monthends(start, end, cal):
    recent_monthends = pd.date_range(start, end, freq='M')
    monthends = [np.datetime64(cal.final_businessday_of_month(m)) for m in recent_monthends]
    logging.info(f"Finished getting np.datetime64 business month ends from {start} to {end} based on {cal}")
    return monthends


def get_datetime_business_monthends(start, end, cal):
    recent_monthends = pd.date_range(start, end, freq='M')
    monthends = [cal.final_businessday_of_month(m) for m in recent_monthends]
    logging.info(f"Finished getting datetime business month ends from {start} to {end} based on {cal}")
    return monthends


def get_datetime_business_days(start, end, cal):
    """
    Return business days based on calendar
    :param start:
    :param end:
    :param cal:
    :return:
    """
    cal_days = pd.date_range(start, end)
    bus_days = [d for d in cal_days if cal.is_business_day(d)]
    logging.info(f"Finished getting business days from {start} to {end} based on {cal}")
    return bus_days


def get_datetime_days(start: datetime.date, end: datetime.date):
    """
    Get date range between two dates
    :param start:
    :param end:
    :return:
    """
    return [d for d in pd.date_range(start, end)]


def generate_now_str_timestamp():
    """
    Generate current timestampe in YYYYMMDD_HHMMSS format and return as string
    :return:
    """
    return datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d_%H%M%S')
