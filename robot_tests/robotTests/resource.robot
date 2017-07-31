*** Settings ***
Documentation     A resource file with reusable keywords and variables.
...
...               The system specific keywords created here form our own
...               domain specific language. They utilize keywords provided
...               by the imported Selenium2Library.
Library           Selenium2Library
Library           DatabaseLibrary

*** Variables ***
${SERVER}         localhost:8001
${BROWSER}        Chrome
${LOGIN URL}      http://${SERVER}/
${WELCOME URL}    http://${SERVER}/
${ERROR URL}      http://${SERVER}/error.html
${ADD_FRIEND_URL}   http://${SERVER}/users/
${REGISTRATION_URL}   http://${SERVER}/register/
${ADMIN_URL}      http://${SERVER}/admin/socialNetworkApp
${USER_MODEL}     user
${DELAY}          0
${USERFRIEND_MODEL}  userfriend
${FRIENDS_PAGE}   http://${SERVER}/friends/
${EDIT_PAGE}    http://${SERVER}/edit/
${IMAGE_FILE_XPATH}   //div[@class="form-row field-profile_image"]//p[@class="file-upload"]//a




*** Keywords ***

Database Connection
    Connect To Database Using Custom Params  psycopg2  database='socialNetwork', user='root', password='hola123', host='localhost', port=5433


Open Browser And Maximize Window
    Open Browser    ${LOGIN URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    ${DELAY}


Login Page Should Be Open
    Title Should Be    Title


Go To Login Page
    Go To    ${LOGIN URL}
    Login Page Should Be Open


Register User
    [Arguments]  ${username_value}  ${password_value}  ${email_value}

    Go To  ${REGISTRATION_URL}
    Input Text    //input[@id="username"]    ${username_value}
    Input Text    //input[@id="password"]    ${password_value}
    Input Text    //input[@id="email"]    ${email_value}

    Click Button    update-submit


Login To UI With Admin
  Input Username    Admin
  Input Password    pass12345
  Submit Credentials


Login To UI With User
  [Arguments]  ${username}  ${password}
  Input Username    ${username}
  Input Password    ${password}
  Submit Credentials


Logout
    Click Element  //div[@class="container"]//a[@id="logout"]


Input Username
    [Arguments]    ${username}
    Input Text    username    ${username}


Input Password
    [Arguments]    ${password}
    Input Text    password   ${password}


Submit Credentials
    Click Button    login-submit


Welcome Page Should Be Open
    Location Should Be    ${WELCOME URL}
    Title Should Be    Title


Go To Add User Page
    Go To    ${ADD_FRIEND_URL}


Go To Admin
    Go To   ${ADMIN_URL}


Go To Edit page
    Go To  ${EDIT_PAGE}


Get User Id From Database
    [Arguments]    ${field}    ${value}
    Check If Exists In Database  SELECT id FROM auth_user WHERE ${field} = '${value}'
    ${query_id}  Query  SELECT id FROM "auth_user" WHERE ${field} = '${value}'
    ${id}  Set Variable  ${query_id[0][0]}
    Return From Keyword    ${id}


Check Admin Textfield
    [Arguments]   ${model}  ${id}  ${field}  ${value}
    Go To    ${ADMIN_URL}/${model}/${id}/
    Wait Until Page Contains Element    //input[@id="id_${field}"]
    Textfield Value Should Be    //input[@id="id_${field}"]    ${value}


Check Admin Emailfield
    [Arguments]   ${model}  ${id}  ${field}  ${value}
    ${current_location}         Get Location
    Go To    ${ADMIN_URL}/${model}/${id}/
    Wait Until Page Contains Element    //input[@id="id_${field}"]
    ${email}  Get Element Attribute    //input[@id="id_email"]@value
    Log  ${value}
    Should Be Equal As Strings    ${email}    ${value}


Check Image Is Added
    [Arguments]   ${model}  ${id}  ${field}  ${value}
    Go To    ${ADMIN_URL}/${model}/${id}/
    Wait Until Page Contains Element    //input[@id="id_${field}"]
    @{image_name}   Split String   ${value}        /
    ${image_value_name}    Set Variable    @{image_name}[-1]
    ${image_value}  Catenate  users/${image_value_name}
    Log  ${image_value}
    Element Text Should Be    ${IMAGE_FILE_XPATH}    ${image_value}
    Check If Exists In Database  SELECT id FROM auth_user WHERE profile_image = '${image_value}'


Check Friend Is Added
   [Arguments]  ${model}  ${id}  ${value}
   Go To    ${ADMIN_URL}/${model}?first_user_id=${id}
   Log  ${value}
   ${second_friend_locator}  Set Variable  //tr[@class="row1"]//th[@class="field-__str__"]//a[.="${value}"]
   ${second_user}  Get Text    ${second_friend_locator}
   Should Be Equal As Strings    ${second_user}    ${value}
   Click Element  ${second_friend_locator}
   ${second_user_id}  Get User Id From Database     username   ${second_user}
   Check If Exists In Database  SELECT id FROM "socialNetworkApp_userfriend" WHERE second_user_id = ${second_user_id} AND first_user_id = ${id}


Check User Exists
    [Arguments]  ${id}
    Check If Exists In Database  SELECT id FROM "auth_user" WHERE id = ${id}

