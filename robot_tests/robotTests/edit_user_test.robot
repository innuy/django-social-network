*** Settings ***
Documentation     A demo test suit
Library           Selenium2Library    timeout=180
Library           String

Resource          resource.robot
Resource          verbose_resource.robot
Library           libraries/ImageModule.py
Library           libraries/hooks.py
Test Teardown     Close Browser
Test Setup        Setup Actions


*** Variables ***
${first_name_field}       first_name
${last_name_field}        last_name
${profile_picture_field}  profile_image
${email_field}            email
${image_path}             /sources/twilio.jpg


*** Keywords ***
Setup Actions
    Database Connection
    Open Browser And Maximize Window
    Register User  RobotTest  Password  test@robotframework.com


Update User
    [Arguments]  ${first_name_value}  ${last_name_value}  ${email_value}  ${username}
    ${user_id}  Get User Id From Database    username   ${username}
    Go To Edit page
    Input Text    //input[@id="firstName"]    ${first_name_value}
    Input Text    //input[@id="lastName"]    ${last_name_value}
    Input Text    //input[@id="email"]    ${email_value}
    Upload Image   ${user_id}   ${image_path}
    Click Button    update-submit


Make User SuperUser
    [Arguments]  ${username}
    Execute Sql String  UPDATE "auth_user" set is_superuser = True WHERE username = '${username}'

Edit User Teardown Actions
    [Arguments]  ${user_id}
    Execute Sql String  DELETE FROM "auth_user" WHERE id = ${user_id}
    Close Browser

*** Test Cases ***

Check User Updated
    Go To Login Page
    Login To UI With User  RobotTest  Password
    Make User SuperUser  RobotTest
    Update User  new first name  new last name  new email  RobotTest

    ${user_id}  Get User Id From Database        username   RobotTest
    Log    ${user_id}

    "${USER_MODEL}" with id "${user_id}" should have image "${profile_picture_field}" "${image_path}"
    "${USER_MODEL}" with id "${user_id}" should have "${first_name_field}" "new first name"
    "${USER_MODEL}" with id "${user_id}" should have "${last_name_field}" "new last name"
    "${USER_MODEL}" with id "${user_id}" and email "new email" should have "${email_field}"
    "${USER_MODEL}" with id "${user_id}" should have "${last_name_field}" "new last name"
    [TearDown]  Edit User Teardown Actions  ${user_id}



