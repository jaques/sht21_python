#!/usr/bin/python
import fcntl
import struct
import time


class SHT31:
    """Class to read temperature and humidity from SHT31, much of class was
    this is based on code from nadanks7 who used
    https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/Humidity_and_Temperature_Sensors/Sensirion_Humidity_and_Temperature_Sensors_SHT3x_Datasheet_digital.pdf
    as well as jaques/SHT21 code from github.

    This does support all features of the sensor, but it will form a reasonable place to start.

    It has been very lightly tested (I don't have the sensor!), but there have been reports of success.
    """

    # control constants
    _RESET = 0x30A2
    _HEATER_ON = 0x306D
    _HEATER_OFF = 0x3066
    _STATUS = 0xF32D
    _TRIGGER = 0x2C06
    _STATUS_BITS_MASK = 0xFFFC

    _I2C_ADDRESS = 0x44

    # From: /linux/i2c-dev.h
    _I2C_SLAVE = 0x0703
    _I2C_SLAVE_FORCE = 0x0706

    # datasheet (v0.93), page 5, table 4
    _MEASUREMENT_WAIT_TIME = 0.015  # (datasheet: typ=12.5, max=15)

    def __init__(self, device_number=1):
        """Opens the i2c device (assuming that the kernel modules have been
        loaded)."""
        self.i2c = open('/dev/i2c-%s' % device_number, 'r+', 0)
        fcntl.ioctl(self.i2c, self._I2C_SLAVE, 0x44)
        time.sleep(0.050)

    def soft_reset(self):
        """Performs Soft Reset on SHT31 chip"""
        self.write(self._RESET)

    def check_heater_status(self):
        """Checks the status of the heater. Returns False if off and True if on"""
        self.write(self._STATUS)

        stats, checksum = struct.unpack(">HB", self.i2c.read(3))
        bit13 = stats & (1 << 13) != 0
        if self._calculate_checksum(stats) == checksum:
            return bit13
        else:
            return "status read failure"

    def turn_heater_on(self):
        """Enables Heater"""
        self.write(self._HEATER_ON)

    def turn_heater_off(self):
        """Disables Heater"""
        self.write(self._HEATER_OFF)

    def get_temp_and_humidity(self, **kwargs):
        """Reads the temperature and humidity - note that this call blocks
        the program for 15ms"""
        unit = kwargs.get('unit', 'C')
        self.write(self._TRIGGER)
        time.sleep(self._MEASUREMENT_WAIT_TIME)
        data = self.i2c.read(6)

        temp_data, temp_checksum, humidity_data, humidity_checksum = struct.unpack(">HBHB", data)

        #  returns a tuple of (temperature, humidity)
        if self._calculate_checksum(temp_data) == temp_checksum and \
           self._calculate_checksum(humidity_data) == humidity_checksum:
            if unit == 'C':
                return self._get_temperature(temp_data), self._get_humidity(humidity_data)
            else:
                return self._get_temperature_fahrenheit(temp_data), self._get_humidity(humidity_data)
        else:
            return 0, 0

    def write(self, value):
        self.i2c.write(struct.pack(">H", value))

    def close(self):
        """Closes the i2c connection"""
        self.i2c.close()

    def __enter__(self):
        """used to enable python's with statement support"""
        return self

    def __exit__(self, *exc_info):
        """with support"""
        self.close()

    @staticmethod
    def _calculate_checksum(value):
        """4.12 Checksum Calculation from an unsigned short input"""
        # CRC
        polynomial = 0x131  # //P(x)=x^8+x^5+x^4+1 = 100110001
        crc = 0xFF

        # calculates 8-Bit checksum with given polynomial
        for byteCtr in [ord(x) for x in struct.pack(">H", value)]:
            crc ^= byteCtr
            for bit in range(8, 0, -1):
                if crc & 0x80:
                    crc = (crc << 1) ^ polynomial
                else:
                    crc = (crc << 1)
        return crc

    @staticmethod
    def _get_temperature(unadjusted):
        """This function reads the first two bytes of data and
        returns the temperature in C by using the following function:
        T = -45 + (175 * (ST/2^16))
        where ST is the value from the sensor
        """
        unadjusted *= 175.0
        unadjusted /= 1 << 16  # divide by 2^16
        unadjusted -= 45
        return unadjusted
    
    @staticmethod
    def _get_temperature_fahrenheit(unadjusted):
        """This function reads the first two bytes of data and
        returns the temperature in C by using the following function:
        T = -49 + (315 * (ST/2^16))
        where ST is the value from the sensor
        """
        unadjusted *= 315.0
        unadjusted /= 1 << 16  # divide by 2^16
        unadjusted -= 49
        return unadjusted

    @staticmethod
    def _get_humidity(unadjusted):
        """This function reads the first two bytes of data and returns
        the relative humidity in percent by using the following function:
        RH = (100 * (SRH / 2 ^16))
        where SRH is the value read from the sensor
        """
        unadjusted *= 100.0
        unadjusted /= 1 << 16  # divide by 2^16
        unadjusted -= 0
        return unadjusted


if __name__ == "__main__":
    try:
        with SHT31(1) as sht31:
            print sht31.check_heater_status()
            sht31.turn_heater_on()
            print sht31.check_heater_status()
            sht31.turn_heater_off()
            print sht31.check_heater_status()
            temperature, humidity = sht31.get_temp_and_humidity()
            print "Temperature C: %s" % temperature
            print "Humidity: %s" % humidity
            temperature, humidity = sht31.get_temp_and_humidity(unit = 'F')
            print "Temperature F: %s" % temperature
            print "Humidity: %s" % humidity
    except IOError, e:
        print e
        print "Error creating connection to i2c.  This must be run as root"

