Feature:
  As a River Pirate
  I want to be able to retrieve the current temperature and humidity readings

  @wip
  Scenario: Retrieving the temperature
    Given that the temperature is as follows:
    | temp | humidity |
    | 24.1 | 33.9     |
    When I create a new reading with the sensor
    Then the reading will be returned with the following values:
    | temperature | humidity |
    | 24.1        | 33.9     |
