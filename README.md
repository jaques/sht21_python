sht21_python
============

Python library for reading data over i2c (tested on raspberry pi)

This is bascially a python port of the c version found here: http://www.emsystech.de/raspi-sht21/

I have only tried it on my first generation raspberry pi (where it seems to work)

Requirements
------------

* i2c must be enabled
* you must run the script as root

To enable i2c check [http://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c].

Depending on your raspberry pi model, you may need to use /dev/i2c-0 or /dev/i2c-1

Usage
-----
    import sht21
    with sht21.SHT21(0) as sht21:
        print "Temperature: %s"%sht21.read_temperature()
        print "Humidity: %s"%sht21.read_humidity()

Note that the number represents the bus number (as discussed).

If you are not root, this is likely to throw IOErrors. Also the calls to `read_xxx()` may also return None
if the checksum fails
