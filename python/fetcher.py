#!/usr/bin/env python

from logging import basicConfig as logging_basicConfig, getLogger, ERROR, DEBUG, CRITICAL
from optparse import OptionParser, OptionGroup
from configobj import ConfigObj
from urllib2 import URLError, urlopen
from json import loads as json_loads
from datetime import datetime

import sensordb

DEFAULT_LOG_LEVEL = ERROR
DEFAULT_CONFIG_FILE = "./fetcher.ini"


class WaisFetcher(object):

    def __init__(self, config_file, logging_level):
        logging_basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = getLogger("WaisFetcher")
        self.logger.setLevel(logging_level)
        self.parse_config(config_file)
        self.db = sensordb.WaisSensorDb(self.database_config, logging_level)

    def parse_config(self, config_file):
        self.logger.debug("Parseig_config")
        try:
            config = ConfigObj(config_file)
            self.database_config = config["database_config"]
            self.prefix = config["prefix"]
            self.timeout = float(config["timeout"])
        except KeyError:
            raise Exception("Invalid config File")
        self.logger.info("Using prefix %s" % self.prefix)
        self.logger.info("Using database config %s" % self.database_config)

    def fetch_json(self, url):
        try:
            self.logger.info("Fetching from %s" % url)
            self.logger.info("Timeout set to %f" % self.timeout)
            return json_loads(urlopen(url, timeout=self.timeout).read())
        except URLError:
            self.logger.error("Unable to get data from %s" % url)
            return None
        except ValueError:
            self.logger.error("Unable to parse Json")
            return None

    def process_reading(self, device, timestamp, data):
        if "internal" in data["reading"].keys():
            self.db.add_internal_temperature_reading(device, timestamp, float(data["reading"]["internal"]))
        if "battery" in data["reading"].keys():
            self.db.add_battery_reading(device, timestamp, float(data["reading"]["battery"]))
        if ("x" in data["reading"].keys() 
                and "y" in data["reading"].keys() 
                and "z" in data["reading"].keys()):
            self.db.add_accelerometer_reading(device, timestamp, 
                int(data["reading"]["x"]), 
                int(data["reading"]["y"]), 
                int(data["reading"]["z"]))
        

    def run(self):
        sensors = self.db.list_sensors()
        timestamp = datetime.utcnow()
        for s in sensors:
            try:
                self.logger.info("Processing %s" % s)
                url = "http://[%s%s]" %(self.prefix, s)
                json = self.fetch_json(url)
                if json is not None:
                    self.process_reading(s, timestamp, json)
            except Exception as e:
                self.logger.error("Unexpected error")
                self.logger.error("%s" % e)





if __name__ == "__main__":
    LOG_LEVEL = DEFAULT_LOG_LEVEL
    PARSER = OptionParser()
    GROUP = OptionGroup(PARSER, "Verbosity Options",
        "Options to change the level of output")
    GROUP.add_option("-q", "--quiet", action="store_true",
        dest="quiet", default=False,
        help="Supress all but critical errors")
    GROUP.add_option("-v", "--verbose", action="store_true",
        dest="verbose", default=False,
        help="Print all information available")
    PARSER.add_option_group(GROUP)
    PARSER.add_option("-c", "--config", action="store",
        type="string", dest="config_file",
        help="Config file containing database credentials")
    (OPTIONS, ARGS) = PARSER.parse_args()
    if OPTIONS.quiet:
        LOG_LEVEL = CRITICAL
    elif OPTIONS.verbose:
        LOG_LEVEL = DEBUG
    if OPTIONS.config_file is None:
        CONFIG = DEFAULT_CONFIG_FILE
    else:
        CONFIG = OPTIONS.config_file
    FETCHER = WaisFetcher(CONFIG, LOG_LEVEL)
    FETCHER.run()

