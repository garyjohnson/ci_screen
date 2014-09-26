Feature: Projects
  As a developer
  I want to see my projects
  So I can know when the build breaks

  Background:
    Given the CI server has projects:
      | name              |
      | My Project        |
      | My Other Project  |
    And the app is running

  Scenario: Show Projects
    Then I see projects "My Project, My Other Project"
