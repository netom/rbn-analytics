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

    for content in fl:
        fname = "data/" + content
        
        zf = zipfile.ZipFile(fname, "r")

        for zipinfo in zf.infolist():
            csvf = zf.open(zipinfo.filename, "r")
            i = 1
            for l in csvf:
                values = l.strip().split(",")
                if values[0] == "callsign" or len(values) <= 1:
                    continue
                values[3] = float(values[3]) # freq
                values[9] = float(values[9]) # db

                oldv10 = values[10]
                values[10] = values[10][0:10] + "T" + values[10][11:19]

                _id = (
                    values[10][0:4] +
                    values[10][5:7] +
                    values[10][8:10] +
                    values[10][11:13] +
                    values[10][14:16] +
                    values[10][17:19] +
                    "%08d" % i
                )

                doc = dict(zip(fields, values))

                yield {
                    '_op_type': 'index',
                    '_index': 'rbn',
                    '_type': 'rbnentry',
                    '_id': _id,
                    '_source': doc
                }

                i += 1
        zf.close()

        print fname

for results in elasticsearch.helpers.streaming_bulk(es, datareader(), chunk_size=5000):
    pass
