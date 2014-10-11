Feature: Projects
  As a developer
  I want to see my projects
  So I can know when the build breaks

  Scenario: Show Projects
    Given I have a CI server with projects:
      | name              |
      | My Project        |
      | My Other Project  |
    And the app is running
    Then I see projects "My Project, My Other Project"

  Scenario: Show Project Status
    Given I have a CI server with projects:
      | name              | status    |
      | My Project        | Success   |
      | My Other Project  | Failure   |
    And the app is running
    Then I see successful projects "My Project"
    And I see failed projects "My Other Project"
    And I do not see failed projects "My Project"
    And I do not see successful projects "My Other Project"

  Scenario: Show Projects from Multiple CI Servers
    Given I have a CI server with projects:
      | name              |
      | My Project        |
    And I have a CI server with projects:
      | name              |
      | My Other Project  |
    And the app is running
    Then I see projects "My Project, My Other Project"

  Scenario: Show failure time for build that just failed
    Given I have a CI server with projects:
      | name        | status    | last_build_time       |
      | My Project  | Failure   | 2014-08-01T11:01:15Z  |
    And the app is running at "2014-08-01 11:01:15"
    Then I see failed projects "My Project"
    And I see "Just Now"

