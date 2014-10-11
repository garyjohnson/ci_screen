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
