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
    
  Scenario: Publishes online status when running
    Given I have MQTT enabled
    And I have a CI server with projects:
      | name              | status    |
      | My Project        | Success   |
    And online topic is set to "/testing/online"
    And the app is running
    Then I get a message:
      | topic             | message   |
      | /testing/online   | 1         |

  Scenario: Publishes offline status when not running
    Given I have MQTT enabled
    And I have a CI server with projects:
      | name              | status    |
      | My Project        | Success   |
    And online topic is set to "/testing/online"
    And the app is running
    And I get a message:
      | topic             | message   |
      | /testing/online   | 1         |
    When I close the app
    Then I get a message:
      | topic             | message   |
      | /testing/online   | 0         |

  Scenario: Shows image published
    Given I have MQTT enabled
    And I have a CI server with projects:
      | name              | status    |
      | My Project        | Success   |
    And marquee topic is set to "/testing/marquee"
    And the app is running
    When I publish a message:
      | topic              | message                                                           |
      | /testing/marquee   | { "image_url":"../../features/assets/1.jpg","duration":5000 } |
    Then I see "../../features/assets/1.jpg"

  Scenario: Removes marquee after duration
    Given I have MQTT enabled
    And I have a CI server with projects:
      | name              | status    |
      | My Project        | Success   |
    And marquee topic is set to "/testing/marquee"
    And the app is running
    When I publish a message:
      | topic              | message                                                           |
      | /testing/marquee   | { "image_url":"../../features/assets/1.jpg","duration":5000 } |
    And I see "../../features/assets/1.jpg"
    And I wait 2 seconds
    Then I do not see "../../features/assets/1.jpg"

  Scenario: Replaces previous published image
    Given I have MQTT enabled
    And I have a CI server with projects:
      | name              | status    |
      | My Project        | Success   |
    And marquee topic is set to "/testing/marquee"
    And the app is running
    When I publish a message:
      | topic              | message                                                           |
      | /testing/marquee   | { "image_url":"../../features/assets/1.jpg","duration":5000 } |
    And I wait 1 second
    And I publish a message:
      | topic              | message                                                           |
      | /testing/marquee   | { "image_url":"../../features/assets/2.jpg","duration":5000 } |
    Then I see "../../features/assets/2.jpg"
