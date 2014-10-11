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
