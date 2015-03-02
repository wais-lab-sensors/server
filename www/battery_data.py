import sys
sys.path.append("/opt/wais-sensor-server/python")
import logging

import sensordb

def index(req):
    req.content_type = "text/csvi"
    database = sensordb.WaisSensorDb("/opt/wais-sensor-server/python/db.ini")
    data = database.get_all_voltages()
    output = ""
    for line in data:
        for cell in line:
            if cell is not None:
                output+= "%s," %cell
            else:
                output+=","
        output += ("\n")
    return output
