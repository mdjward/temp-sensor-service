from .device import Device
from abc import ABC, abstractmethod
import Adafruit_DHT.common as Adafruit_DHT_common
from typing import Callable

class AdafruitSensorConfiguration:

    _nameTypeMappings = {
        'DHT11': Adafruit_DHT_common.DHT11,
        'DHT22': Adafruit_DHT_common.DHT22,
        'AM2302': Adafruit_DHT_common.AM2302,
    }

    _deviceType = None
    _gpioPin = None

    def __init__(self, deviceType:int, gpioPin:int):
        if deviceType not in Adafruit_DHT_common.SENSORS:
            raise ValueError("Unrecognised device type %u" % (deviceType))
        if gpioPin < 1:
            raise ValueError("GPIO pin must be given as an integer greater than 0")

        self._deviceType = deviceType
        self._gpioPin = gpioPin

    def getDeviceType(self):
        return self._deviceType

    def getGpioPin(self):
        return self._gpioPin

    def fromNameAndGpioPin(deviceName:str, gpioPin:int):
        if deviceName in AdafruitSensorConfiguration._nameTypeMappings:
            return AdafruitSensorConfiguration(AdafruitSensorConfiguration._nameTypeMappings[deviceName], gpioPin)
        
        raise ValueError("Unrecognised device name %s" % deviceName)



class AbstractSensor(ABC):
    @abstractmethod
    def getReadings(self):
        pass



class AdafruitSensor(AbstractSensor):
    _device = None
    _configuration = None
    _reader = None

    def __init__(
        self,
        device:Device,
        configuration:AdafruitSensorConfiguration,
        reader:Callable=None
    ):
        self._device = device
        self._configuration = configuration
        self._reader = reader if reader is not None else Adafruit_DHT_common.get_platform().read_retry

    def getReadings(self):
        (humid, temp) = self._reader(
            self._configuration.getDeviceType(),
            self._configuration.getGpioPin()
        )

        return {
            "temperature": temp,
            "humidity": humid,
        }

    def configureDetectedDevice(
        configuration:AdafruitSensorConfiguration
    ):
        return AdafruitSensor(Device.detect(), configuration)
