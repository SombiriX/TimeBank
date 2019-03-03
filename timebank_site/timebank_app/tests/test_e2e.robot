*** Variables ***


*** Settings ***
Documentation   Tests Timebank end to end
Resource        resources/common.robot    # common test vars, keywords, etc
Test Teardown   Manage Flush
Suite Setup     Start Django and open Browser
Suite Teardown  Stop Django and close Browser

*** Keywords ***


*** Test Cases ***
Scenario: As a visitor I can visit the django default page
  Go To  ${SERVER}
  Wait until page contains element  id=app
