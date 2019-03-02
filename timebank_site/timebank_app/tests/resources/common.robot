*** Variables ***
${HOSTNAME}     127.0.0.1
${PORT}         55001
${SERVER}       http://${HOSTNAME}:${PORT}/
${BROWSER}      chrome
${SANDBOX}      --verbose

*** Settings ***
Documentation   Django Robot Tests
Library         SeleniumLibrary  timeout=10  implicit_wait=0
Library         DjangoLibrary  ${HOSTNAME}  ${PORT}  path=timebank_site/timebank_site  manage=timebank_site/manage.py  settings=timebank_site.settings

*** Keywords ***
Start Django and open Browser
  Start Django
  # Open Browser  ${SERVER}  ${BROWSER}
  ${list} =     Create List    ${SANDBOX}
  ${args} =     Create Dictionary    args=${list}
  ${desired caps} =     Create Dictionary    chromeOptions=${args}
  Open Browser    ${SERVER}    browser=${BROWSER}    desired_capabilities=${desired caps}

Stop Django and close browser
  Close Browser
  Stop Django
