from Adafruit_DHT import common as Adafruit_DHT_common
from Adafruit_DHT import platform_detect as platform
from dht22_temp_sensor_service.sensor import *
from dht22_temp_sensor_service.device import *
from unittest import TestCase
from unittest_data_provider import data_provider
from types import ModuleType



class AdafruitSensorConfigurationTest(TestCase):

    acceptedDeviceTypes = lambda: [
        [Adafruit_DHT_common.DHT11, 1],
        [Adafruit_DHT_common.DHT22, 2],
        [Adafruit_DHT_common.AM2302, 3],
    ]

    acceptedDeviceTypeNames = lambda: [
        ['DHT11', Adafruit_DHT_common.DHT11, 1],
        ['DHT22', Adafruit_DHT_common.DHT22, 2],
        ['AM2302', Adafruit_DHT_common.AM2302, 3],
    ]

    def test_constructor_will_raise_value_error_if_unrecognized_device_type_given(self):
        with self.assertRaises(ValueError):
            AdafruitSensorConfiguration(0, 1)

    def test_constructor_will_raise_value_error_if_unrecognized_gpio_pin_given(self):
        with self.assertRaises(ValueError):
            AdafruitSensorConfiguration(Adafruit_DHT_common.DHT22, 0)

    @data_provider(acceptedDeviceTypes)
    def test_constructor_will_assign_accepted_values(self, deviceType:int, gpioPin:int):
        device = AdafruitSensorConfiguration(deviceType, gpioPin)

        self.assertEqual(deviceType, device.getDeviceType())
        self.assertEqual(gpioPin, device.getGpioPin())

    @data_provider(acceptedDeviceTypeNames)
    def it_will_resolve_device_name_to_device_type_identifier(self, deviceTypeName:str, deviceType:int, gpioPin:int):
        device = AdafruitSensorConfiguration.fromNameAndGpioPin(deviceTypeName, gpioPin)

        self.assertEqual(deviceType, device.getDeviceType())
        self.assertEqual(gpioPin, device.getGpioPin())

    def it_will_raise_value_error_if_device_name_not_recognised(self):
        with self.assertRaises(ValueError):
            AdafruitSensorConfiguration.fromNameAndGpioPin("DHT-something-something", 1)



class DummyModule(dict):
    def __init__(self, *args, **kwargs):
        super(DummyModule, self).__init__(*args, **kwargs)
        self.__dict__ = self



class AdafruitSensorTest(TestCase):

    def test_it_will_defer_to_injected_callable(self):
        expectedReadings = (30, 40)

        sensor = AdafruitSensor(
            RaspberryPiDevice(2, 3),
            AdafruitSensorConfiguration.fromNameAndGpioPin('DHT22', 4),
            lambda deviceType, gpioPin: expectedReadings
        )

        actualReadings = sensor.getReadings()

        self.assertEqual(expectedReadings[0], actualReadings['temperature'])
        self.assertEqual(expectedReadings[1], actualReadings['humidity'])



class AdafruitSensorFullIntegrationTest(TestCase):
    _skip = False

    devices = lambda: [
        [platform.RASPBERRY_PI, "Raspberry Pi"],
        [platform.BEAGLEBONE_BLACK, "Beaglebone Black"],
    ]

    @data_provider(devices)
    def test_sensor_will_return_actual_readings(self, device:int, deviceName:str):
        if platform.platform_detect() != device:
            self.skipTest("Unable to perform full sensor test as current device is not a %s" % deviceName)

        sensor = AdafruitSensor.configureDetectedDevice(
            AdafruitSensorConfiguration.fromNameAndGpioPin('DHT22', 4)
        )

        self.assertIsInstance(AdafruitSensor, sensor)

        actualReadings = sensor.getReadings()

        self.assertGreaterEqual(0, actualReadings['temperature'])
        self.assertGreaterEqual(0, actualReadings['humidity'])
