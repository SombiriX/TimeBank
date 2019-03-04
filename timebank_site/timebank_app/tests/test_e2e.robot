*** Variables ***
${USERNAME}         TEST_USER
${USERNAME2}        TEST_USER2
${PASSWD}           qweasdzx
${EMAIL}            test@example.com
${EMAIL2}            test2@example.com
${SUBMIT}           xpath:.//button[@type='submit']
${BASE APP}         id:app
# Toolbar
${LOGIN BTN}        xpath:.//a[@href='/login']
${CREATE BTN}       xpath:.//a[@href='/register']
${TIMEBANK BTN}     xpath:.//a[@href='/timebank']
# Login
${LOGIN VIEW}       id:login-view
${LOGIN URL}        ${SERVER}/login
${USERNAME IPT}     xpath:.//input[@aria-label='Username']
${PASSWD IPT}       xpath:.//input[@aria-label='Password']
${PASSWD2 IPT}      xpath:.//input[@aria-label='Confirm Password']
${EMAIL IPT}        xpath:.//input[@aria-label='Email']
# User Registration
${CREATE URL}       ${SERVER}/register
${CREATE ACC BTN}   ${SUBMIT}
${CREATE VIEW}      id:register-view
${ERROR1}           xpath:.//div[contains(@class, 'error')]/div[contains(., 'USERNAME') and contains(., 'EMAIL')]
${ERROR2}           xpath:.//div[contains(@class, 'error')]/div[contains(., 'USERNAME')]
${ERROR3}           xpath:.//div[contains(@class, 'error')]/div[contains(., 'EMAIL')]
${SUCCESS}          xpath:.//div[contains(@class, 'success')]

*** Settings ***
Documentation   Tests Timebank end to end
Resource        resources/common.robot    # common test vars, keywords, etc
Suite Setup     Start Django and open Browser
Suite Teardown  Stop Django and close Browser

*** Keywords ***


*** Test Cases ***
Can visit the base page
  Go To  ${SERVER}
  Wait until page contains element  ${BASE APP}

Cannot login with invalid credentials
  Click With Retry      ${LOGIN BTN}
  Page Should Be Open   ${LOGIN URL}      ${LOGIN VIEW}
  Clear and Input       ${USERNAME IPT}   ${USERNAME}
  Clear and Input       ${PASSWD IPT}     ${PASSWD}
  Click Element         ${SUBMIT}
  Location Should Be With Retry    ${SERVER}/

Can create a user
  Click With Retry      ${CREATE BTN}
  Page Should Be Open   ${CREATE URL}     ${CREATE VIEW}
  Clear and Input       ${EMAIL IPT}      ${EMAIL}
  Clear and Input       ${USERNAME IPT}   ${USERNAME}
  Clear and Input       ${PASSWD IPT}     ${PASSWD}
  Clear and Input       ${PASSWD2 IPT}    ${PASSWD}
  Click Element         ${SUBMIT}
  Wait Until Element Is Visible           ${SUCCESS}
  Sleep                 7s

Cannot create user with existing username and email
  Click With Retry      ${CREATE BTN}
  Page Should Be Open   ${CREATE URL}     ${CREATE VIEW}
  Clear and Input       ${EMAIL IPT}      ${EMAIL}
  Clear and Input       ${USERNAME IPT}   ${USERNAME}
  Clear and Input       ${PASSWD IPT}     ${PASSWD}
  Clear and Input       ${PASSWD2 IPT}    ${PASSWD}
  Click Element         ${SUBMIT}
  Wait Until Element Is Visible           ${ERROR1}
  Sleep                 7s

Cannot create user with existing username
  Click With Retry      ${CREATE BTN}
  Page Should Be Open   ${CREATE URL}     ${CREATE VIEW}
  Clear and Input       ${EMAIL IPT}      ${EMAIL2}
  Clear and Input       ${USERNAME IPT}   ${USERNAME}
  Clear and Input       ${PASSWD IPT}     ${PASSWD}
  Clear and Input       ${PASSWD2 IPT}    ${PASSWD}
  Click Element         ${SUBMIT}
  Wait Until Element Is Visible           ${ERROR2}
  Sleep                 7s

Cannot create user with existing email
  Click With Retry      ${CREATE BTN}
  Page Should Be Open   ${CREATE URL}     ${CREATE VIEW}
  Clear and Input       ${EMAIL IPT}      ${EMAIL}
  Clear and Input       ${USERNAME IPT}   ${USERNAME2}
  Clear and Input       ${PASSWD IPT}     ${PASSWD}
  Clear and Input       ${PASSWD2 IPT}    ${PASSWD}
  Click Element         ${SUBMIT}
  Wait Until Element Is Visible           ${ERROR3}
  Sleep                 7s

Can login with valid credentials
  Click With Retry      ${LOGIN BTN}
  Page Should Be Open   ${LOGIN URL}      ${LOGIN VIEW}
  Clear and Input       ${USERNAME IPT}   ${USERNAME}
  Clear and Input       ${PASSWD IPT}     ${PASSWD}
  Click Element         ${SUBMIT}
  Location Should Be With Retry           ${SERVER}/
  Wait Until Element Is Visible           ${TIMEBANK BTN}
