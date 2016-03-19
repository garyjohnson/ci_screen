Feature: MQTT

  Scenario: Does not connect to MQTT by default
    Given I do not have MQTT enabled
    And I have a CI server with projects:
      | name              | status    |
      | My Project        | Success   |
    And the app is running
    Then the app does not connect to MQTT

  Scenario: Connects to MQTT when enabled
    Given I have MQTT enabled
    And I have a CI server with projects:
      | name              | status    |
      | My Project        | Success   |
    And the app is running
    Then the app connects to MQTT

  Scenario: Displays now playing info
    Given I have MQTT enabled
    And I have a CI server with projects:
      | name              | status    |
      | My Project        | Success   |
    And now playing topic is set to "/testing/now_playing"
    And the app is running
    When I publish now playing info to "/testing/now_playing":
      | song       | artist          | album         | album art                               |
      | These Days | The Black Keys  | Brothers      | http://lorempixel.com/500/500/abstract/ |
    Then I see now playing info:
      | song       | artist          | album art                               |
      | These Days | The Black Keys  | http://lorempixel.com/500/500/abstract/ |
    
