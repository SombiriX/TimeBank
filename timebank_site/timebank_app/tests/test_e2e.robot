*** Variables ***


*** Settings ***
Documentation   Tests Timebank end to end
Resource        resources/common.robot    # common test vars, keywords, etc
Test Teardown   Clear DB

*** Keywords ***


*** Test Cases ***
Scenario: As a visitor I can visit the django default page
  Go To  ${SERVER}
  Wait until page contains element  id=app
