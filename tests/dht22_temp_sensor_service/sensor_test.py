from unittest import TestCase
from Adafruit_DHT import platform_detect as dht
from dht22_temp_sensor_service.sensor import DHT22Sensor



class AdafruitSensorConfigurationTest(TestCase):
    

    pass



class AdafruitSensorTest(TestCase):
    _skip = False

    def setUpClass():
        if dht.platform_detect() == dht.UNKNOWN:
            AdafruitSensorTest._skip = True

    def setUp(self):
        if (AdafruitSensorTest._skip == True):
            self.skipTest("Unable to run functional tests on unsupported hardware device")

    def test_sensor_will_return_actual_readings(self):
        sensor = DHT22Sensor()

        pass
