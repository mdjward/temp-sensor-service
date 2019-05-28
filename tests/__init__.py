import unittest, sys

def my_module_suite():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(tests.adafruit_temp_sensor_service)

    return suite
