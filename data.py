# -*- coding: utf-8 -*-
#
# Author   : Martin Užák <martin.uzak@gmail.com>
# Creation : 2017-01-04 16:08
# File     : data.py

"""
data structures for TTT
"""

import datetime


# default date formats
DATE_FMT     = "%Y-%m-%d"
TIME_FMT     = "%H:%M"
DATETIME_FMT = DATE_FMT + " " + TIME_FMT


class Time_Interval:
    """ Model a time interval on the same day. 

    >>> ti = Time_Interval("2016-11-21", "11:11", "14:04")
    >>> ti
    2016-11-21 11:11 - 14:04
    >>> int(ti)
    173
    >>> ti = Time_Interval("2016-11-21", "9", "14:05")
    >>> ti
    2016-11-21 09:00 - 14:05
    >>> int(ti)
    305
    """

    def __init__(self, date, time_from, time_to):
        # normalize input:
        # add minutes if missing
        add_min_fmt = "%s:00" 
        if not ":" in time_from:
            time_from = add_min_fmt % time_from
        if not ":" in time_to:
            time_to = add_min_fmt % time_to

        # initialize
        fmt        = "%s %%s" % date
        self.date  = date
        self.start = datetime.datetime.strptime(fmt % time_from, DATETIME_FMT)
        self.end   = datetime.datetime.strptime(fmt % time_to, DATETIME_FMT)

    def __int__(self):
        "return the difference of `self.start` to `self.end` in minutes"
        return (self.end - self.start).seconds // 60

    def __repr__(self):
        return "%s %s - %s" % (
            self.date,
            self.start.strftime(TIME_FMT), 
            self.end.strftime(TIME_FMT))
    __str__ = __repr__


class Time_Value:
    """Model a time value composed of any number of hours and minutes

    >>> tv = Time_Value("5h 10m")
    >>> tv
    5h10m
    >>> int(tv)
    310
    >>> tv = Time_Value("130m")
    >>> tv
    2h10m
    >>> int(tv)
    130
    """
    def __init__(self, value):
        if "h" in value:
            hours, mins = value.split("h")
            hours = int(hours.strip())
        else:
            hours = 0
            mins = value
        self.hours = hours
        self.mins = 0
        if mins:
            self.mins = int(mins.split("m")[0])
        while self.mins >= 60:
            self.mins -= 60
            self.hours += 1

    def __int__(self):
        "return the difference of `self.start` to `self.end` in minutes"
        return self.hours * 60 + self.mins

    def __repr__(self):
        if self.mins:
            return "%dh%dm" % (self.hours, self.mins)
        return "%dh" % (self.hours)
    __str___ = __repr__


class Entry:
    def __init__(self, date, value, cost_center, desc):
        self.date        = date
        self.value       = value 
        self.cost_center = cost_center
        self.desc        = desc

    def __repr__(self):
        return "%s %13s %6s %s" % \
                (self.date.strftime(DATE_FMT), 
                 self.value, 
                 self.cost_center, 
                 self.desc)
    __str__ = __repr__


def create_cost_center(project, phase):
    return "%s:%s" % (project, phase)


if __name__ == "__main__":
    import doctest, data
    doctest.testmod(data)
