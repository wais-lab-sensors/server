from configobj import ConfigObj
import mysql.connector
import logging

class WaisSensorDb(object):
    def __init__(self, config_file="./db.ini", logging_level=logging.ERROR):
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
            db = mysql.connector.connect(host=host, user=user,
            password=password, database=database)
            self.logger.info("Connected to database %s on %s" %(database, host))
            self.db = db
        except mysql.connector.Error as e:
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
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM devices;")
        sensors = cursor.fetchall()
        cursor.close()
        ret = []
        for s in sensors:
            if(not check_enabled) or (check_enabled and s[1]):
                ret.append(s[0])
        return ret

    def get_current_locations(self):
        if not self.connected():
            raise DbError()
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM current_locations;")
        locations = cursor.fetchall()
        cursor.close()
        return locations

    def add_internal_temperature_reading(self, device, timestamp, reading):
        self.logger.debug("Adding %s %s %f to internal temperature readings"
            % (device, timestamp, reading))
        if self.db is None:
            raise DbError()
        else:
            cursor = self.db.cursor()
            cursor.execute(
                "INSERT IGNORE INTO internal_temperature_readings (device, timestamp,value) VALUES (%s, %s, %s)",
                (device.lower(), timestamp, reading))
            cursor.close()
            self.db.commit()
            self.logger.debug("Temperature stored")

    def add_battery_reading(self, device, timestamp, reading):
        self.logger.debug("Adding %s %s %f to battery readings"
            % (device, timestamp, reading))
        if self.db is None:
            raise DbError()
        else:
            cursor = self.db.cursor()
            cursor.execute(
                "INSERT IGNORE INTO battery_readings (device, timestamp,value) VALUES (%s, %s, %s)",
                (device.lower(), timestamp, reading))
            cursor.close()
            self.db.commit()
            self.logger.debug("Voltage stored")

    def add_accelerometer_reading(self, device, timestamp, x, y , z):
        self.logger.debug("Adding %s %s %d %d %d to accelerometer readings"
            % (device, timestamp, x, y, z))
        if self.db is None:
            raise DbError()
        else:
            cursor = self.db.cursor()
            cursor.execute(
                "INSERT IGNORE INTO accelerometer_readings (device, timestamp,x, y, z) VALUES (%s, %s, %s, %s, %s)",
                (device.lower(), timestamp, x, y, z))
            cursor.close()
            self.db.commit()
            self.logger.debug("accelerometer stored")

    def add_temperature_reading(self, device, timestamp, reading):
        self.logger.debug("Adding %s %s %f to temperature readings"
            % (device, timestamp, reading))
        if self.db is None:
            raise DbError()
        else:
            cursor = self.db.cursor()
            cursor.execute(
                "INSERT IGNORE INTO temperature_readings (device, timestamp,value) VALUES (%s, %s, %s)",
                (device.lower(), timestamp, reading))
            cursor.close()
            self.db.commit()
            self.logger.debug("Temperature stored")

    def add_humidity_reading(self, device, timestamp, reading):
        self.logger.debug("Adding %s %s %f to humidity readings"
            % (device, timestamp, reading))
        if self.db is None:
            raise DbError()
        else:
            cursor = self.db.cursor()
            cursor.execute(
                "INSERT IGNORE INTO humidity_readings (device, timestamp,value) VALUES (%s, %s, %s)",
                (device.lower(), timestamp, reading))
            cursor.close()
            self.db.commit()
            self.logger.debug("Humidity stored")

    def get_all_internal_temperatures(self):
        self.logger.debug("Getting internal temperatures")
        sensors = self.list_sensors(False)
        data_raw = {}
        for s in sensors:
            temperature_raw = self.get_internal_temperatures(s)
            for d in temperature_raw:
                device = d[0]
                timestamp = d[1]
                value = d[2]
                if not timestamp in data_raw.keys():
                    #not a previously seen timestamp
                    data_raw[timestamp] = {}
                data_raw[timestamp][device] = value
        header = []
        data = []
        data.append(header)
        header.append("timestamp")
        header.extend(sensors)
        timestamps = sorted(data_raw.keys())
        for t in timestamps:
            a = []
            a.append(t)
            for s in sensors:
                try:
                    a.append(data_raw[t][s])
                except KeyError:
                    a.append(None)
            data.append(a)
        return data

    def get_all_temperatures(self):
        self.logger.debug("Getting temperatures")
        sensors = self.list_sensors(False)
        data_raw = {}
        for s in sensors:
            temperature_raw = self.get_temperatures(s)
            for d in temperature_raw:
                device = d[0]
                timestamp = d[1]
                value = d[2]
                if not timestamp in data_raw.keys():
                    #not a previously seen timestamp
                    data_raw[timestamp] = {}
                data_raw[timestamp][device] = value
        header = []
        data = []
        data.append(header)
        header.append("timestamp")
        header.extend(sensors)
        timestamps = sorted(data_raw.keys())
        for t in timestamps:
            a = []
            a.append(t)
            for s in sensors:
                try:
                    a.append(data_raw[t][s])
                except KeyError:
                    a.append(None)
            data.append(a)
        return data

    def get_all_humidities(self):
        self.logger.debug("Getting humidities")
        sensors = self.list_sensors(False)
        data_raw = {}
        for s in sensors:
            humidity_raw = self.get_humidities(s)
            for d in humidity_raw:
                device = d[0]
                timestamp = d[1]
                value = d[2]
                if not timestamp in data_raw.keys():
                    #not a previously seen timestamp
                    data_raw[timestamp] = {}
                data_raw[timestamp][device] = value
        header = []
        data = []
        data.append(header)
        header.append("timestamp")
        header.extend(sensors)
        timestamps = sorted(data_raw.keys())
        for t in timestamps:
            a = []
            a.append(t)
            for s in sensors:
                try:
                    a.append(data_raw[t][s])
                except KeyError:
                    a.append(None)
            data.append(a)
        return data

    def get_all_voltages(self):
        self.logger.debug("Getting voltages")
        sensors = self.list_sensors(False)
        data_raw = {}
        for s in sensors:
            voltage_raw= self.get_voltages(s)
            for d in voltage_raw:
                device = d[0]
                timestamp = d[1]
                value = d[2]
                if not timestamp in data_raw.keys():
                    #not a previously seen timestamp
                    data_raw[timestamp] = {}
                data_raw[timestamp][device] = value
        header = []
        data = []
        data.append(header)
        header.append("timestamp")
        header.extend(sensors)
        timestamps = sorted(data_raw.keys())
        for t in timestamps:
            a = []
            a.append(t)
            for s in sensors:
                try:
                    a.append(data_raw[t][s])
                except KeyError:
                    a.append(None)
            data.append(a)
        return data

    def get_internal_temperatures(self, device):
        if not self.connected():
            raise DbError()
        cursor = self.db.cursor()
        cursor.execute("SELECT device, timestamp, value FROM internal_temperature_readings WHERE device = '%s';" % device.lower())
        temps = cursor.fetchall()
        cursor.close()
        return temps

    def get_temperatures(self, device):
        if not self.connected():
            raise DbError()
        cursor = self.db.cursor()
        cursor.execute("SELECT device, timestamp, value FROM temperature_readings WHERE device = '%s';" % device.lower())
        temps = cursor.fetchall()
        cursor.close()
        return temps
    
    def get_humidities(self, device):
        if not self.connected():
            raise DbError()
        cursor = self.db.cursor()
        cursor.execute("SELECT device, timestamp, value FROM humidity_readings WHERE device = '%s';" % device.lower())
        humidities = cursor.fetchall()
        cursor.close()
        return humidities

    def get_voltages(self, device):
        if not self.connected():
            raise DbError()
        cursor = self.db.cursor()
        cursor.execute("SELECT device, timestamp, value FROM battery_readings WHERE device = '%s';" % device.lower())
        volts = cursor.fetchall()
        cursor.close()
        return volts
    
    def __del__(self):
        self.logger.debug("Closing db connection")
        self.db.close()



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
