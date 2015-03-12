import sys
sys.path.append("/opt/wais-sensor-server/python")
import logging

import sensordb

def index(req):
    req.content_type = "text/plain"
    database = sensordb.WaisSensorDb("/opt/wais-sensor-server/python/db.ini")
    data = database.get_current_locations()
    output = "{\n"
    #for line in data:
    #    output +="\"%s\":\"%s\",\n" %(line[0], line[1])
    #output += "}"
    i = 0
    while i < len(data):
        output +=  "\"%s\":\"%s\"" % (data[i][0], data[i][1])
        if i < (len(data) -1):
            output += ",\n"
        else:
            output +="\n"
        i+= 1
    output += "}"
    return output
