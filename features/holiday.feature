@wip
Feature: Holiday

  Scenario: No snow before winter
    Given I have holiday effects enabled
    And I have a CI server with projects:
      | name              | status    |
      | My Project        | Success   |
      | My Other Project  | Success   |
    And the app is running at "2014-11-14 01:01:01" UTC
    Then I do not see snow

  Scenario: No snow after winter
    Given I have holiday effects enabled
    And I have a CI server with projects:
      | name              | status    |
      | My Project        | Success   |
      | My Other Project  | Success   |
    And the app is running at "2014-12-26 01:01:01" UTC
    Then I do not see snow

  Scenario: Snow at beginning of winter
    Given I have holiday effects enabled
    And I have a CI server with projects:
      | name              | status    |
      | My Project        | Success   |
      | My Other Project  | Success   |
    And the app is running at "2014-11-15 01:01:01" UTC
    Then I see snow

  Scenario: Snow at end of winter
    Given I have holiday effects enabled
    And I have a CI server with projects:
      | name              | status    |
      | My Project        | Success   |
      | My Other Project  | Success   |
    And the app is running at "2014-12-25 01:01:01" UTC
    Then I see snow
