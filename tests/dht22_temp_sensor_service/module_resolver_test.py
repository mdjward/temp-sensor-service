from setuptools import Extension
from unittest import TestCase
import Adafruit_DHT
from unittest_data_provider import data_provider
from dht22_temp_sensor_service.device import *
from dht22_temp_sensor_service.module_resolver import *

TEST_MODULE = {
    'read': lambda sensor, pin: (None, None)
}
Adafruit_DHT.Raspberry_Pi = TEST_MODULE
Adafruit_DHT.Raspberry_Pi_2 = TEST_MODULE
Adafruit_DHT.Beaglebone_Black = TEST_MODULE



class AdafruitModuleResolverTest(TestCase):

    examples = lambda: (
        [RaspberryPiDevice(1, 1), Adafruit_DHT.Raspberry_Pi],
        [RaspberryPiDevice(2, 2), Adafruit_DHT.Raspberry_Pi_2],
        [RaspberryPiDevice(2, 3), Adafruit_DHT.Raspberry_Pi_2],
        [BeagleboneBlackDevice(), Adafruit_DHT.Raspberry_Pi_2],
    )

    @data_provider(examples)
    def test_resolve_will_yield_correct_module(self, deviceType:Device, targetModule):
        prev = Adafruit_DHT.common.get_platform

        self.assertEqual(targetModule, AdafruitModuleResolver().resolve(deviceType))

        Adafruit_DHT.common.get_platform = prev
