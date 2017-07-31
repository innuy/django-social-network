*** Settings ***
Documentation     A test suite with a single test for valid login.
...
...               This test has a workflow that is created using keywords in
...               the imported resource file.
Resource          resource.robot

*** Settings ***
Test Setup  Database Connection

*** Test Cases ***
Valid login
  Open Browser And Maximize Window
  Go To Login Page
  Input Username    Admin
  Input Password    pass12345
  Submit Credentials
  Welcome Page Should Be Open
  [TearDown]  Close Browser
