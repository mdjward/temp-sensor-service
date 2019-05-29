from .sensor import AbstractSensor
from abc import ABC, abstractmethod
from flask import Flask, Response, json
from flask.views import MethodView

class AbstractServiceFactory(ABC):
    @abstractmethod
    def createApp(self):
        pass



class FlaskReadingResource(MethodView):
    _sensor = None

    def __init__(self, sensor:AbstractSensor):
        self._sensor = sensor

    def post(self):
        return Response(json.dumps(self._sensor.getReadings()))



class FlaskServiceFactory(AbstractServiceFactory):
    _sensor = None
    _appName = None

    def __init__(self, sensor:AbstractSensor, appName:str='temp_sensor_service'):
        self._sensor = sensor
        self._appName = appName

    def createApp(self):
        app = Flask(self._appName)

        readingResourceView = FlaskReadingResource.as_view('reading', self._sensor)
        app.add_url_rule('/reading', defaults={}, view_func=readingResourceView, methods=['POST',])

        return app
