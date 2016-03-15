Feature: MQTT

  Scenario: Does not connect to MQTT by default
    Given I do not have MQTT enabled
    And I have a CI server with projects:
      | name              | status    |
      | My Project        | Success   |
    And the app is running
    Then the app does not connect to MQTT
