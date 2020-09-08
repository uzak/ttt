#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author   : Martin Užák <martin.uzak@gmail.com>
# Creation : 2017-01-02 16:57
# File     : ttt.py

"""
driver and main class for `Time Tracking Tool` (also known as TTT)
"""

import argparse
import functools
import logging
import datetime
import collections
import re

from data import *

# line parser
DATE        = r"(\d{1,}-\d{1,2}-\d{1,2})"
TIME        = r"(\d{1,2}(?::\d{1,2})?)"
TIME_VALUE  = r"(?:(?:" + TIME + r"\s*-\s*" + TIME + r")|(\d+h(?:\s?\d+m)?|\d+m))"
PRJ_ABBR    = r"(\w+)"
PHASE       = r"(\d+)"
COST_CENTER = PRJ_ABBR+":"+PHASE
DESCRIPTION = r"(.*)"
LINE_PAT    = re.compile \
    (
        DATE +
        r"\s+"
        + TIME_VALUE +
        r"\s+"
        + COST_CENTER +
        r"(?:\s+" + DESCRIPTION + ")?"
    )


class InvalidInputError(ValueError):
    def __init__(self, file, line, message):
        super(InvalidInputError, self).__init__()
        self.file    = file
        self.line    = line
        self.message = message

    def __str__(self):
        return "%s:%s> %s" % (self.file, self.line, self.message)


class TTT:
    "Time Tracking Tool"

    def __init__(self, from_date=None, to_date=None):
        self.data      = [] 
        self.from_date = self._make_date(from_date)
        self.to_date   = self._make_date(to_date)

    def read(self, filename):
        # read input data
        with open(filename, 'r') as f:
            for i, line in enumerate(f):
                self.parse_line(line, filename, i)

        # filter out all data outside of requested interval (from_dt, to_dt)
        if self.from_date:
            self.data = filter(lambda x: x.date >= self.from_date.date(), self.data)
        if self.to_date:
            self.data = filter(lambda x: x.date < self.to_date, self.data)

    def parse_line(self, line, filename, line_no):
        "Parse `line` from `filename` and return an `Entry` object if possible"
        line = line.strip()

        # get rid of comments
        line = line.split("#")[0]

        if line:
            m = LINE_PAT.match(line)
            if m:
                date, start, end, val, prj, phase, desc = m.groups()
                date = datetime.datetime.strptime(date, DATE_FMT).date()
                cc   = create_cost_center(prj, phase)
                if start and end:
                    val = Time_Interval(date, start, end)
                else:
                    val = Time_Value(val)
                entry = Entry(date, val, cc, desc)
                self.data.append(entry)
            else:
                raise InvalidInputError(filename, line_no, line)

    def output_csv(self):
        for monthly in self.by_months(self.data).values():
            for by_cc in self.by_cost_center(monthly).values():
                year   = by_cc[0].date.year
                month  = by_cc[0].date.month
                cc     = by_cc[0].cost_center
                values = [int(r.value) for r in by_cc]
                total  = functools.reduce(lambda a, b: a+b, values)
                print("%d,%d,%s,%d" % (year, month, cc, total))

    def output_human_readable(self):
        "output read data in human readable form"
        data = self.data
        fmt = "\t{:<10} {:>10}"

        # print month by month stats
        for month, entries in self.by_months(data).items():
            print("* %s" % month)
            for cc, entries_by_cc in self.by_cost_center(entries).items():
                print(fmt.format(cc, self.sum(entries_by_cc)))
            print(fmt.format("=>", self.sum(entries)))
            print()

        # print totals
        data = list(data) #XXX
        if data:
            start = min(data, key=lambda x: x.date)
            end = max(data, key=lambda x: x.date)
            print("%s..........%s" % (
                start.date.strftime(DATE_FMT), end.date.strftime(DATE_FMT)))
            print("-" * 30)
            for cc, entries_by_cc in self.by_cost_center(data).items():
                print(fmt.format(cc, self.sum(entries_by_cc)))
            print("=" * 30)
            print("Total %17s" % self.sum(data))


    def sum(self, data):
        """return human readble sum of all values in data"""
        val = 0
        for row in data:
            val += int(row.value)
        h = val // 60
        m = val % 60
        if m:
            return "{:>3}h {:>2}min".format(h, m)
        return "{:>3}h        ".format(h)

    def by_cost_center(self, data):
        """split `data` by cost centers and return as dictionary"""
        result = collections.OrderedDict()
        for row in sorted(data, key=lambda x: x.cost_center):
            cc = row.cost_center
            if cc not in result:
                result[cc] = []
            result[cc].append(row)
        return result

    def by_months(self, data):
        """return `data` grouped by months"""
        result = collections.OrderedDict()
        for row in sorted(data, key=lambda x: x.date):
            key = "%s %s" % (row.date.strftime("%B"), row.date.year)
            if key not in result:
                result[key] = []
            result[key].append(row)
        return result

    def _make_date(self, strvalue):
        if not strvalue:
            return
        try:
            result = datetime.datetime.strptime(strvalue, DATE_FMT)
        except ValueError:
            raise ValueError("Invalid date value: `%s`" % strvalue)
        return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--from_date")
    parser.add_argument("--to_date")
    parser.add_argument("filename", nargs="+", help="input text file")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-hr", dest="output_hr", action='store_true')
    group.add_argument("-csv", dest="output_csv", action='store_true')
    args = parser.parse_args()

    logging.debug("args.from_date: %s" % args.from_date)
    logging.debug("args.to_date: %s"% args.to_date)
    logging.debug("args.filename: %s" % args.filename)

    ttt = TTT(from_date=args.from_date, to_date=args.to_date)

    # read input
    for fn in args.filename:
        ttt.read(fn)

    # output
    if args.output_hr:
        ttt.output_human_readable()
    elif args.output_csv:
        ttt.output_csv()
    
if __name__ == "__main__":
    main()
