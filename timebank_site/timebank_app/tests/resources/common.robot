*** Variables ***
${HOSTNAME}     127.0.0.1
${PORT}         8001
${SERVER}       http://${HOSTNAME}:${PORT}
${BROWSER}      chrome
${SANDBOX}      --verbose
# App
${BASE APP}         id:app
# Toolbar
${LOGIN BTN}        xpath:.//a[@href='/login']
${CREATE BTN}       xpath:.//a[@href='/register']
${TIMEBANK BTN}     xpath:.//a[@href='/timebank']

*** Settings ***
Documentation   Django Robot Tests
Library         SeleniumLibrary   timeout=10  implicit_wait=3
Library         DjangoLibrary     ${HOSTNAME}  ${PORT}  path=timebank_site/timebank_site  manage=timebank_site/manage.py  settings=timebank_site.settings

*** Keywords ***
Click With Retry
  [Documentation]  Click the specified element until success or timeout
  [Arguments]                   ${elem}  ${wait}=5 sec  ${tries}=3x
  Wait Until Keyword Succeeds   ${tries}  ${wait}  Click Element  ${elem}

Location Should Be With Retry
  [Documentation]  Checks location until success or timeout
  [Arguments]                   ${location}  ${wait}=5 sec  ${tries}=3x
  Wait Until Keyword Succeeds   ${tries}  ${wait}  Location Should Be  ${location}

Page Should Be Open
  [Documentation]                     Tests whether a page has opened correctly
  [Arguments]                         ${location}   ${locator}=tag:body
  Wait Until Element Is Visible       ${locator}    10 seconds
  Location Should Contain             ${location}

Start Django and open Browser
  Start Django
  ${list} =     Create List    ${SANDBOX}  --no-default-browser-check  --no-first-run  --disable-default-apps
  ${args} =     Create Dictionary    args=${list}
  ${desired caps} =     Create Dictionary    chromeOptions=${args}
  Open Browser    ${SERVER}    browser=${BROWSER}    desired_capabilities=${desired caps}

Stop Django and close browser
  Close Browser
  Stop Django

Clear and Input
  [Documentation]         Clears an input field before entering a value
  [Arguments]             ${locator}  ${value}
  FOR   ${i}  IN RANGE    20
    Press Keys              ${locator}  BACKSPACE
  END
  Input Text              ${locator}  ${value}
