Feature:
  As a human being who thrives in room temperatures of approximately 20 degrees celsius
  I want to be able to retrieve the current temperature and humidity readings

  Scenario: Retrieving the temperature
    Given that the temperature is as follows:
    | temp | humidity |
    | 24.1 | 33.9     |
    When I create a new reading with a DHT22 sensor on a Raspberry Pi 2 version 3 using GPIO pin 4
    Then the reading will be returned with the following values:
    | temperature | humidity |
    | 24.1        | 33.9     |
