from abc import ABC, abstractmethod
import Adafruit_DHT

class AbstractSensor(ABC):
    @abstractmethod
    def getReadings(self):
        pass

class DHT22Sensor(AbstractSensor):
    def __init__(self):
        pass

    def getReadings(self):
        return {"temperature": 0, "humidity": 0}
