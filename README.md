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

Depending on your raspberry pi model, you may need to use `/dev/i2c-0` for the older model or `/dev/i2c-1`
for the newer models.

Usage
-----

    import sht21
    with sht21.SHT21(0) as sht21:
        print "Temperature: %s"%sht21.read_temperature()
        print "Humidity: %s"%sht21.read_humidity()

Note that the `0` represents the i2c bus number (as discussed), to use `/dev/i2c-1` on a newer Raspberry Pi
you need to update the device number:

    with sht21.SHT21(1) as sht21:

Note: If you are not root, this is likely to throw IOErrors. Also be aware that the calls 
to `read_temperature()` or `read_humidity()` may return `None` if the checksum fails.
