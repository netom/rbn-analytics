#!/usr/bin/env python
#-*- coding: utf8 -*-

import json
import os
import zipfile

outf = open("data/rbn-data.json", "w")

fl = []

fields = ["callsign","de_pfx","de_cont","freq","band","dx","dx_pfx","dx_cont","mode","db","date","speed","tx_mode"]

for content in os.listdir("data"):
    if content[0] == ".":
        continue

    fl.append(content)

fl.sort()

for content in fl:
    fname = "data/" + content

    zf = zipfile.ZipFile(fname, "r")

    for zipinfo in zf.infolist():
        csvf = zf.open(zipinfo.filename, "r")
        for l in csvf:
            values = l.strip().split(",")
            if values[0] == "callsign" or len(values) <= 1:
                continue
            values[3] = float(values[3]) # freq
            values[9] = float(values[9]) # db
            outf.write(json.dumps(dict(zip(fields, values))) + "\n")
    zf.close()

    print fname

outf.close()
