Feature: Projects
  As a developer
  I want to see my projects
  So I can know when the build breaks

  Scenario: Show Projects
    Given the CI server has projects:
      | name              |
      | My Project        |
      | My Other Project  |
    And the app is running
    Then I see projects "My Project, My Other Project"

  Scenario: Show Project Status
    Given the CI server has projects:
      | name              | status    |
      | My Project        | Success   |
      | My Other Project  | Failure   |
    And the app is running
    Then I see successful projects "My Project"
    And I see failed projects "My Other Project"
    And I do not see failed projects "My Project"
    And I do not see successful projects "My Other Project"
