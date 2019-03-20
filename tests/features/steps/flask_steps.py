from flask import Flask, request, Response, json
from behave import given, when, then
from helpers.client import app
from helpers.mocksensor import mock

client = app.test_client()

@given('that the temperature is as follows')
def given_that_the_temperature_is_as_follows(context):
    context.lastResponse = None

    for row in context.table:
        mock.setReadings(float(row['temp']), float(row['humidity']))
        return

@when('I create a new reading with the sensor')
def when_i_create_a_new_reading_with_the_sensor(context):
    context.lastResponse = client.post('/reading')

@then('the reading will be returned with the following values')
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
