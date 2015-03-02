#!/usr/bin/env python
import logging
from optparse import OptionParser, OptionGroup
from configobj import ConfigObj

import sensordb

DEFAULT_LOG_LEVEL = logging.ERROR
DEFAULT_CONFIG_FILE = "./fetcher.ini"

class WaisFetcher(object):

    def __init__(self, config_file, logging_level):
        logging.basicConfig()
        self.logger = logging.getLogger("WaisFetcher")
        self.logger.setLevel(logging_level)
        self.parse_config(config_file)
        self.db = sensordb.WaisSensorDb(self.database_config, logging_level)

    def parse_config(self, config_file):
        self.logger.debug("Parseig_config")
        try:
            config = ConfigObj(config_file)
            self.database_config = config["database_config"]
            self.prefix = config["prefix"]
        except KeyError:
            raise Exception("Invalid config File")
        self.logger.info("Using prefix %s" % self.prefix)
        self.logger.info("Using database config %s" % self.database_config)

    def run(self):
    	print "%s" % self.db.list_sensors()


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
        LOG_LEVEL = logging.CRITICAL
    elif OPTIONS.verbose:
        LOG_LEVEL = logging.DEBUG
    if OPTIONS.config_file is None:
        CONFIG = DEFAULT_CONFIG_FILE
    else:
        CONFIG = OPTIONS.config_file
    FETCHER = WaisFetcher(CONFIG, LOG_LEVEL)
    FETCHER.run()

