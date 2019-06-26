from adafruit_temp_sensor_service.service import FlaskServiceFactory
from adafruit_temp_sensor_service.sensor import AdafruitSensor, AdafruitSensorConfiguration
import os, sys

if 'ADAFRUIT_GPIO_PIN' not in os.environ or 'ADAFRUIT_DEVICE_NAME' not in os.environ:
    print("Environment variables ADAFRUIT_DEVICE_NAME and ADAFRUIT_GPIO_PIN must be set")
    sys.exit(1)

app = FlaskServiceFactory(
    AdafruitSensor.configureDetectedDevice(
        AdafruitSensorConfiguration.fromNameAndGpioPin(
            os.environ.get('ADAFRUIT_DEVICE_NAME'),
            int(os.environ.get('ADAFRUIT_GPIO_PIN'))
        )
    ),
    os.environ.get('ADAFRUIT_SENSOR_SERVICE_NAME', 'adafruit-temp-sensor-service')
).createApp()
