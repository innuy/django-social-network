*** Settings ***
Documentation     A demo test suit
Library           Selenium2Library    timeout=180
Library           String

Resource          resource.robot
Resource          verbose_resource.robot
Test Teardown     Close Browser
Test Setup        Database Connection


*** Test Cases ***
Create Valid User
    Open Browser And Maximize Window
    Register User  Example  Password  example@example.com
    Login To UI With Admin
    ${user_id}  Get User Id From Database    username   Example

    "User with id "${user_id}" should exist"
    [Teardown]  Execute Sql String  DELETE FROM "auth_user" WHERE id = ${user_id}
                Close Browser


