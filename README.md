sht21_python
============

Python library for reading data over i2c for a Sensirion SHT21 (tested on Raspberry Pi).

This is a python port of the c version found here: http://www.emsystech.de/raspi-sht21/

I have only tried it on my first generation Raspberry Pi, but there have been reports of this 
working on newer Raspberry Pis.  This code should also work with all sensors in the SHT2x series;
there have been report of it working with a SHT25.

Requirements
------------

* i2c must be enabled
* you must run the script as root

To enable i2c check http://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c

Depending on your raspberry pi model, you may need to use `/dev/i2c-0` or
`/dev/i2c-1`

Usage
-----

    import sht21
    with sht21.SHT21(0) as sht21:
        print "Temperature: %s"%sht21.read_temperature()
        print "Humidity: %s"%sht21.read_humidity()

Note that the `0` represents the i2c bus number (as discussed), to use
`/dev/i2c-1` on a newer Raspberry Pi you need to update the device number:

If you are not root, this is likely to throw IOErrors. Also the calls to
`read_xxx()` may also return None if the checksum fails

sht31_python
============

Thanks to the kind contribution of an initial version by @nadanks7 and some
testing by @jimbowarrior there is now also a basic implementation for the sht31
sensor.  More work is required here to support all features of the sensor, but
the initial framework is in place.

Usage is similar, but as reading temerature and humidity is now a single
operation there is single call to do that.

Note that in this example we are using `/dev/i2c-1`.

    import sht31
    with sht31.SHT31(1) as sht31:
        print sht31.check_heater_status()
        sht31.turn_heater_on()
        print sht31.check_heater_status()
        sht31.turn_heater_off()
        print sht31.check_heater_status()
        temperature, humidity = sht31.get_temp_and_humidity()
        print "Temperature: %s" % temperature
        print "Humidity: %s" % humidity


