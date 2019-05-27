from .device import *
import Adafruit_DHT

class AdafruitModuleResolver:
    def resolve(self, deviceType:Device):
        if (isinstance(deviceType, RaspberryPiDevice)):
            return self._resolveRaspberryPi(deviceType)

        if (isinstance(deviceType, BeagleboneBlackDevice)):
            return Adafruit_DHT.Beaglebone_Black

    def _resolveRaspberryPi(self, deviceType:RaspberryPiDevice):
        version = deviceType.getVersion()

        if version == 1:
            return Adafruit_DHT.Raspberry_Pi
        if version == 2 or version == 3:
            return Adafruit_DHT.Raspberry_Pi_2

        return None
