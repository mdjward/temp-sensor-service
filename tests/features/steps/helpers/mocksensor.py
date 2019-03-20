class MockSensor:
    _temp = 0.00
    _humidity = 0.00

    def setReadings(self, temp:float, humidity:float):
        self._temp = temp
        self._humidity = humidity

    def getReadings(self):
        return {"temperature": self._temp, "humidity": self._humidity}

mock = MockSensor()
