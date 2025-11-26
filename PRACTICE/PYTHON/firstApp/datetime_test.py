# -*- coding: utf-8 -*-
from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta


def main():
    ##DATETIME OBJECTS
    #Get today's date from datetime class
    today = datetime.now()
    print(date.today())
    print(today)
    # Get the current time
    t = datetime.time(datetime.now())
    print("The current time is",t)
    #weekday returns 0 (monday) through 6 (sunday)
    wd = date.weekday(today)
    #Days start at 0 for monday
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday",
    "sunday"]
    print("Today is day number %d" % wd + " which is a " + days[wd])

#%c - local date and time, %x-local's date, %X- local's time
    ##### Time Formatting ####
    #%I/%H - 12/24 Hour, %M - minute, %S - second, %p - local's AM/PM
    print(today.strftime("%I:%M:%S %p"))  # 12-Hour:Minute:Second:AM
    print(today.strftime("%H:%M:%S"))  # 24-Hour:Minute:Second
    print(today.strftime("%A, %d %B %Y"))

    # print today's date one year from now
    print("one year from now it will be:" + str(today + timedelta(days=365)))

    # How many days until New Year's Day?
    today = date.today()  # get todays date
    fnyd = date(today.year + 1, 1, 1)  # get New Year Day for the same year
    pnyd = date(today.year, 1, 1)  # get New Year Day for the same year
    cd = date(today.year, 12, 24)
    # use date comparison to see if New Year Day has already gone for this year
    # if it has, use the replace() function to get the date for next year
    if fnyd > today and today > pnyd:
        print("New Year day will be in %d days" % ((fnyd - today).days))
        print("Last New Year day was %d days ago" % ((today - pnyd).days))
    if cd > today:
        print("Christmas will be in %d days" % ((cd - today).days))
    else:
        print("Christmas was %d days ago" % ((today - cd).days))

if __name__ == "__main__":
    main()