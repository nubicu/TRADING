# -*- coding: utf-8 -*-
import calendar
# Create a plain text calendar
tc = calendar.TextCalendar(calendar.MONDAY)
cal = tc.formatmonth(2020, 4, 0, 0)
print(cal)

# Create an HTML formatted calendar
hc = calendar.HTMLCalendar(calendar.MONDAY)
cal = hc.formatmonth(2020, 4)
print(cal)

# loop over the days of a month
# zeroes indicate that the day of the week is in a next month or overlapping month
#for i in c.itermonthdays(2025, 1):
#    print(i)

# The calendar can give info based on local such aS names of days and months
# (full and abbreviated forms)
for name in calendar.month_name:
    print(name)
print
for day in calendar.day_name:
    print(day)
print
# calculate days based on a rule: Ex an audit day on the second Monday of every month
# Figure out what days would be for each month, we can use the script as shown here
for month in range(1, 13):
# It retrieves a list of weeks that represent the month
    mycal = calendar.monthcalendar(2021, month)
# The second MONDAY has to be within the first two weeks
    week1 = mycal[1]
    week2 = mycal[2]
    if week1[calendar.MONDAY] != 0:
        auditday = week1[calendar.MONDAY]
    else:
# if the second MONDAY isn't in the first week, it must be in the second week
        auditday = week2[calendar.MONDAY]
print("Audit day is : %9s %2d" % (calendar.month_name[month], auditday))