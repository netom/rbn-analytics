#!/usr/bin/env python

import datetime
import os
import sys
import urllib2

url_template = "http://www.reversebeacon.net/raw_data/dl.php?f=%s"

first_date   = datetime.date(2009, 02, 21)
current_date = datetime.date.today()

a_day = datetime.timedelta(1)

d = first_date
while d < current_date:
    datestr = "%d%02d%02d" % (d.year, d.month, d.day)
    fname = "data/" + datestr + ".zip"

    if os.path.exists(fname):
        print "File %s exists" % fname
        d += a_day
        continue

    url = url_template % datestr

    try:
        sys.stdout.write("Fetching %s..." % url)
        sys.stdout.flush()
        response = urllib2.urlopen(url)
        with open(fname, "wb") as output:
            output.write(response.read())
        print " done."
    except urllib2.HTTPError as e:
        print "Error: %s" % e.reason

    d += a_day
