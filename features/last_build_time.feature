Feature: Last Time Built
  As a developer
  I want to know when my builds failed
  So I can know how long they have been broken for

  Scenario: Show failure time for build that just failed
    Given I have a CI server with projects:
      | name        | status    | last_build_time       |
      | My Project  | Failure   | 2014-08-01T11:01:15Z  |
    And the app is running at "2014-08-01 11:01:15"
    Then I see failed projects "My Project"
    And I see "Just Now"

  Scenario: Show failure time for build a minute ago
    Given I have a CI server with projects:
      | name        | status    | last_build_time       |
      | My Project  | Failure   | 2014-08-01T11:01:15Z  |
    And the app is running at "2014-08-01 11:02:15"
    Then I see failed projects "My Project"
    And I see "1 minute ago"

  Scenario: Show failure time for build multiple minutes ago
    Given I have a CI server with projects:
      | name        | status    | last_build_time       |
      | My Project  | Failure   | 2014-08-01T11:01:15Z  |
    And the app is running at "2014-08-01 11:04:15"
    Then I see failed projects "My Project"
    And I see "3 minutes ago"

  Scenario: Show failure time for build an hour ago
    Given I have a CI server with projects:
      | name        | status    | last_build_time       |
      | My Project  | Failure   | 2014-08-01T11:01:15Z  |
    And the app is running at "2014-08-01 12:15:15"
    Then I see failed projects "My Project"
    And I see "1 hour ago"

  Scenario: Show failure time for build multiple hours ago
    Given I have a CI server with projects:
      | name        | status    | last_build_time       |
      | My Project  | Failure   | 2014-08-01T11:01:15Z  |
    And the app is running at "2014-08-01 14:15:15"
    Then I see failed projects "My Project"
    And I see "3 hours ago"

  Scenario: Show failure time for build a day ago
    Given I have a CI server with projects:
      | name        | status    | last_build_time       |
      | My Project  | Failure   | 2014-08-01T11:01:15Z  |
    And the app is running at "2014-08-02 12:15:15"
    Then I see failed projects "My Project"
    And I see "1 day ago"

  Scenario: Show failure time for build multiple days ago
    Given I have a CI server with projects:
      | name        | status    | last_build_time       |
      | My Project  | Failure   | 2014-08-02T11:01:15Z  |
    And the app is running at "2014-08-15 12:15:15"
    Then I see failed projects "My Project"
    And I see "13 days ago"

  @wip
  Scenario: Sort successful builds by last build time
    Given I have a CI server with projects:
      | name            | status    | last_build_time       |
      | My Project 1  | Success   | 2013-08-02T11:01:15Z  |
      | My Project 2  | Success   | 2014-08-02T11:01:15Z  |
    And I have a CI server with projects:
      | name            | status    | last_build_time       |
      | My Project 3  | Success   | 2014-01-01T11:01:15Z  |
    And my poll rate is 1 seconds
    And the app is running at "2014-08-15 12:15:15"
    Then "My Project 2" is above "My Project 3"
    And "My Project 3" is above "My Project 1"
