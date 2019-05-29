from flask import Flask, request, Response, json
from behave import given, when, then, use_step_matcher
from adafruit_temp_sensor_service.device import RaspberryPiDevice, BeagleboneBlackDevice
from adafruit_temp_sensor_service.sensor import AdafruitSensorConfiguration, AdafruitSensor
from adafruit_temp_sensor_service.service import FlaskServiceFactory

use_step_matcher("re")

class MockData:
    temp = 0.00
    humidity = 0.00

deviceMap = {
    "Raspberry Pi": lambda revision, version: RaspberryPiDevice(int(revision), int(version)),
    "Beaglebone Black": lambda revision, version: BeagleboneBlackDevice(),
}



@given(u'that the temperature is as follows')
def given_that_the_temperature_is_as_follows(context):
    context.lastResponse = None

    for row in context.table:
        MockData.temp = float(row['temp'])
        MockData.humidity = float(row['humidity'])
        return

@when(u'I create a new reading with a (?P<deviceTypeName>[A-Z0-9]+) sensor on a (?P<device>(?:\w+)(?: \w+))(?: (?P<revision>[0-9]+) version (?P<version>[0-9]+))? using GPIO pin (?P<gpioPin>[0-9]+)')
def when_i_create_a_new_reading_with_the_sensor(
    context,
    deviceTypeName:str,
    device:str,
    revision:int = None,
    version:int = None,
    gpioPin:int = None
):
    sensor = AdafruitSensor(
        deviceMap[device](revision, version),
        AdafruitSensorConfiguration.fromNameAndGpioPin(deviceTypeName, int(gpioPin)),
        lambda deviceType, gpioPin: (MockData.temp, MockData.humidity)
    )
    client = FlaskServiceFactory(sensor, 'test').createApp().test_client()
    context.lastResponse = client.post('/reading')

@then(u'the reading will be returned with the following values')
def then_the_reading_will_be_returned(context):
    assert isinstance(context.lastResponse, Response)
    assert context.lastResponse.status_code == 201 or context.lastResponse.status_code == 200

    response_data = json.loads(context.lastResponse.data)

    for row in context.table:
        for heading in row.headings:
            assert heading in response_data
            assert isinstance(response_data[heading], float)
            assert response_data[heading] == float(row[heading])
        return
