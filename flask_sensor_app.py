from adafruit_temp_sensor_service.service import FlaskServiceFactory
from adafruit_temp_sensor_service.sensor import AdafruitSensor, AdafruitSensorConfiguration
import sys

number_of_args = len(sys.argv)
if number_of_args < 2:
    raise RuntimeError("Usage: %s device_name gpio_pin_number [app-name]" % sys.argv[0])
    sys.exit(1)

app = FlaskServiceFactory(
    sys.argv[3] if number_of_args > 2 else "adafruit-temp-sensor-service",
    AdafruitSensor.configureDetectedDevice(
        AdafruitSensorConfiguration.fromNameAndGpioPin(
            sys.argv[1],
            int(sys.argv[2])
        )
    )
).createApp()
