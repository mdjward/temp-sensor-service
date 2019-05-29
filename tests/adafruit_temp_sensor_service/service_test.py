import sys
from flask import Flask as App, Response, json
from unittest import TestCase
from unittest_data_provider import data_provider
from adafruit_temp_sensor_service.device import RaspberryPiDevice
from adafruit_temp_sensor_service.sensor import AdafruitSensor, AdafruitSensorConfiguration
from adafruit_temp_sensor_service.service import FlaskServiceFactory



class FlaskServiceTest(TestCase):

    def test_it_will_create_and_configure_an_app_with_a_mock_sensor(self):
        temp = 25.0
        humid = 30.0
        reader = lambda deviceType, gpioPin: (temp, humid)

        config = AdafruitSensorConfiguration.fromNameAndGpioPin('DHT22', 4)
        device = RaspberryPiDevice(2, 3)
        sensor = AdafruitSensor(device, config, reader)

        app = FlaskServiceFactory(sensor).createApp()
        self.assertIsInstance(app, App)

        response = app.test_client().post('/reading')
        self.assertIsInstance(response, Response)

        response_data = json.loads(response.data)

        self.assertEqual(temp, response_data['temperature'])
        self.assertEqual(humid, response_data['humidity'])
