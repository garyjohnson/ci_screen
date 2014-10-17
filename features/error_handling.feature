Feature: Error Handling
  As a developer
  I want to see my projects even if I can't reach a CI server
  So that a temporary failure will not take down the CI wall

  Scenario: Show projects from non-failing CI server
    Given I have a CI server with projects:
      | name              |
      | My Project        |
    And I have a CI server with projects:
      | name              |
      | My Other Project  |
    And CI server 2 is failing
    And the app is running
    Then I see projects "My Project"
    And I do not see projects "My Other Project"

  Scenario: Do not remove projects from failing CI server
    Given I have a CI server with projects:
      | name              |
      | My Project        |
    And I have a CI server with projects:
      | name              |
      | My Other Project  |
    And my poll rate is 1 seconds
    And the app is running
    And I see projects "My Project"
    And I see projects "My Other Project"
    When CI server 2 is failing
    And I wait 2 seconds
    Then I see projects "My Project"
    And I see projects "My Other Project"
  
