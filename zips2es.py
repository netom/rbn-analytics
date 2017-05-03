#!/usr/bin/env python
#-*- coding: utf8 -*-

import datetime
import elasticsearch
import elasticsearch.helpers
import json
import os
import time
import zipfile

es = elasticsearch.Elasticsearch(['http://elastic:changeme@localhost:9200/'])

def datareader():
    fl = []

    fields = ["callsign","de_pfx","de_cont","freq","band","dx","dx_pfx","dx_cont","mode","db","date","speed","tx_mode"]

    for content in os.listdir("data"):
        if content[0] == ".":
            continue

        fl.append(content)

    fl.sort()

    i = 1
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

                values[10] = datetime.datetime.strptime(values[10][:19], '%Y-%m-%d %H:%M:%S')

                doc = dict(zip(fields, values))

                yield {
                    '_op_type': 'index',
                    '_index': 'rbn',
                    '_type': 'rbnentry',
                    '_id': i,
                    '_source': doc
                }

                i += 1
        zf.close()

        print fname

for results in elasticsearch.helpers.streaming_bulk(es, datareader()):
    pass
