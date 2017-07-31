*** Settings ***
Documentation     A demo test suit
Library           Selenium2Library    timeout=180
Library           String
Resource          resource.robot
Resource          verbose_resource.robot
Library           libraries/hooks.py
Test Teardown     Close Browser

*** Settings ***
Test Setup  Setup Tests


*** Keywords ***

Setup Tests
    Database Connection


Add New Friend From UI
    [Arguments]  ${friends_name}
    Go To   ${ADD_FRIEND_URL}
    Wait Until Page Contains Element  //li[contains(text(),${friends_name})]//button
    Click Element    //li[contains(text(),${friends_name})]//button


Check Friend Is Already Added
    [Arguments]  ${friends_name}
    Go To   ${ADD_FRIEND_URL}
    Page Should Not Contain Element   //li[contains(text(),${friends_name})]//button


Go To Friends page
    Go To  ${FRIENDS_PAGE}


Teardown Duplicated Friendships
    [Arguments]  ${first_user_id}  ${second_user_id}  ${third_user_id}
    Execute Sql String  DELETE FROM "socialNetworkApp_userfriend" WHERE second_user_id = ${second_user_id} AND first_user_id = ${first_user_id}
    Execute Sql String  DELETE FROM "socialNetworkApp_userfriend" WHERE second_user_id = ${third_user_id} AND first_user_id = ${first_user_id}
    Execute Sql String  DELETE FROM "auth_user" WHERE id = ${second_user_id}
    Execute Sql String  DELETE FROM "auth_user" WHERE id = ${first_user_id}
    Execute Sql String  DELETE FROM "auth_user" WHERE id = ${third_user_id}
    Close Browser

*** Test Cases ***

Add Friend Test
  Open Browser And Maximize Window
  Go To Login Page
  Login To UI With Admin

  Add New Friend From UI  "Bob"
  Go To Admin

  ${user_id}  Get User Id From Database     username   Admin
  ${second_user_id}  Get User Id From Database     username   Bob
  "${USERFRIEND_MODEL}" with id "${user_id}" should have as friend "Bob"
  [Teardown]  Execute Sql String  DELETE FROM "socialNetworkApp_userfriend" WHERE second_user_id = ${second_user_id} AND first_user_id = ${user_id}
              Close Browser


Check Duplicated Friendships
    Open Browser And Maximize Window
    Register User  FirstExample  Password  example1@example.com
    Register User  SecondExample  Password  example2@example.com
    Register User  ThirdExample  Password  example3@example.com

    ${first_user_id}  Get User Id From Database   username   FirstExample
    Log  ${first_user_id}
    ${second_user_id}  Get User Id From Database   username   SecondExample
    ${third_user_id}  Get User Id From Database   username   ThirdExample

    Login To UI With User  FirstExample  Password

    Add New Friend From UI  "SecondExample"
    Sleep  1s
    Add New Friend From UI  "ThirdExample"

    Logout
    Wait Until Page Contains Element  //input[@id="username"]
    Login To UI With User  SecondExample  Password
    Check Friend Is Already Added  "FirstExample"

    [Teardown]   Teardown Duplicated Friendships  ${first_user_id}  ${second_user_id}  ${third_user_id}







