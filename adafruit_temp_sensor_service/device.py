from abc import ABC, abstractmethod
from Adafruit_DHT import platform_detect as platform
from typing import Callable

class Device(ABC):

    @abstractmethod
    def getIdentifier(self):
        pass

    def detect(
        platform_detector:Callable[[], int]=platform.platform_detect,
        revision_detector:Callable[[], int]=platform.pi_revision,
        version_detector:Callable[[], int]=platform.pi_version
    ):
        result = platform_detector()

        if result == platform.RASPBERRY_PI:
            return RaspberryPiDevice(revision_detector(), version_detector())

        if result == platform.BEAGLEBONE_BLACK:
            return BeagleboneBlackDevice()

        raise(UnknownDeviceException("Could not detect host device"))



class RaspberryPiDevice(Device):

    _revision = None
    _version = None

    def __init__(self, revision:int, version:int):
        if revision <= 0 or revision > 2:
            raise ValueError("Revision must be between 1 and 2 inclusive")
        if version <= 0 or version > 3:
            raise ValueError("Version must be between 1 and 3 inclusive")

        self._revision = revision
        self._version = version

    def getIdentifier(self):
        return platform.RASPBERRY_PI

    def getRevision(self):
        return self._revision

    def getVersion(self):
        return self._version

    def getDeviceInfo(self):
        return {
            "name": "Raspberry Pi",
            "revision": self._revision,
            "version": self._version
        }



class BeagleboneBlackDevice(Device):

    def getIdentifier(self):
        return platform.BEAGLEBONE_BLACK

    def getDeviceInfo(self):
        return {"name": "Beaglebone Black"}



class UnknownDeviceException(Exception):
    pass
