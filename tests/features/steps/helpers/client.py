from flask import Flask, Response, json
from flask.views import MethodView
from helpers.mocksensor import mock

mock.getReadings()
app = Flask('test')

class ReadingResource(MethodView):
    def post(self):
        return Response(json.dumps(mock.getReadings()))

reading_resource_view = ReadingResource.as_view('reading')
app.add_url_rule('/reading', defaults={}, view_func=reading_resource_view, methods=['POST',])
