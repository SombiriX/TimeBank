*** Variables ***


*** Settings ***
Documentation   Tests Timebank end to end
Resource        timebank_site/timebank_app/tests/resources/common.robot    # Test setup and teardown
Test Teardown   Clear DB

*** Keywords ***


*** Test Cases ***
Scenario: As a visitor I can visit the django default page
  Go To  ${SERVER}
  Wait until page contains element  id=app
