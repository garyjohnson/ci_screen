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
    And the app is running at "2014-03-01 01:01:01" UTC
    Then I do not see snow

  Scenario: Snow at beginning of winter
    Given I have holiday effects enabled
    And I have a CI server with projects:
      | name              | status    |
      | My Project        | Success   |
      | My Other Project  | Success   |
    And the app is running at "2014-12-01 01:01:01" UTC
    Then I see snow

  Scenario: Snow at end of winter
    Given I have holiday effects enabled
    And I have a CI server with projects:
      | name              | status    |
      | My Project        | Success   |
      | My Other Project  | Success   |
    And the app is running at "2014-12-25 01:01:01" UTC
    Then I see snow

  Scenario: Hearts on week of valentine's day
    Given I have holiday effects enabled
    And I have a CI server with projects:
      | name              | status    |
      | My Project        | Success   |
      | My Other Project  | Success   |
    And the app is running at "2015-02-09 01:01:01" UTC
    Then I see hearts

  Scenario: Hearts on valentine's day
    Given I have holiday effects enabled
    And I have a CI server with projects:
      | name              | status    |
      | My Project        | Success   |
      | My Other Project  | Success   |
    And the app is running at "2015-02-14 01:01:01" UTC
    Then I see hearts

  Scenario: No hearts before week of valentine's day
    Given I have holiday effects enabled
    And I have a CI server with projects:
      | name              | status    |
      | My Project        | Success   |
      | My Other Project  | Success   |
    And the app is running at "2015-02-08 01:01:01" UTC
    Then I do not see hearts

  Scenario: No hearts after valentine's day
    Given I have holiday effects enabled
    And I have a CI server with projects:
      | name              | status    |
      | My Project        | Success   |
      | My Other Project  | Success   |
    And the app is running at "2015-02-15 01:01:01" UTC
    Then I do not see hearts

  Scenario: Weird stuff on april fools
    Given I have holiday effects enabled
    And I have a CI server with projects:
      | name              | status    |
      | My Project        | Success   |
      | My Other Project  | Success   |
    And the app is running at "2020-04-01 01:01:01" UTC
    Then I see weird stuff

