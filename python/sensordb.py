from configobj import ConfigObj
import MySQLdb
import logging

class WaisSenseDb(object):
    def __init__(self, config_file, logging_level=logging.ERROR):
        logging.basicConfig()
        self.logger = logging.getLogger("WaisSenseDb")
        self.logger.setLevel(logging_level)
        self.logger.debug("Loading database config")
        self.db_config = DbConfig(config_file)
        self.db = None
        self.connect()

    def connect(self):
        host = self.db_config.server
        user = self.db_config.user
        password = self.db_config.password
        database = self.db_config.database
        try:
            db = MySQLdb.connect(host=host, user=user,
            passwd=password, db=database)
            self.logger.info("Connected to database %s on %s" %(database, host))
            self.db = db
        except MySQLdb.Error, e:
            self.logger.critical("Unable to connect to db %s on %s as user %s" %
            (database, host, user))
            self.logger.critical(e)
            raise DbError(str(e))

    def connected(self):
        return self.db is not None

    def list_sensors(self, check_enabled=True):
        """
            If check enabled is true it only includes device that are
            enabled, otherwise all devices are returned
        """
        if not self.connected():
            raise DbError()
        self.db.query("SELECT * FROM devices;")
        sensors = self.db.store_result().fetch_row(0)
        ret = []
        for s in sensors:
            if(not check_enabled) or (check_enabled and s[1]):
                ret.append(s[0])
        return ret

    def add_internal_temperature_reading(self, device, timestamp, reading):
        self.logger.debug("Adding %s %s %f to internal temperature readings"
            % (device, timestamp, reading))
        if self.db is None:
            raise DbError()
        else:
            cursor = self.db.cursor()
            cursor.execute(
            "INSERT IGNORE INTO internal_temperature_readings (device, timestamp,value) VALUES (%s, %s, %s)",
            (device, timestamp, reading))
            cursor.close()
            self.db.commit()
            self.logger.debug("Temperature stored")



class DbConfig(object):
    """
    A class containing the connection information required to access the
    database
    """
    def __init__(self, config_file):
        """
        Read the config file and extract the required information
        """
        try:
            config = ConfigObj(config_file)
            self.database = config["database"]
            self.server = config["server"]
            self.user = config["user"]
            self.password = config["pass"]
        except KeyError:
            raise ConfigError("Invalid config File")

class ConfigError(Exception):
    """
    An error for when something has gone wrong reading the config
    """
    pass

class DbError(Exception):
    pass
