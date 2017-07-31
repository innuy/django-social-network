*** Settings ***
Documentation     A resource file with reusable keywords and variables.
...
Resource          resource.robot

Library           Selenium2Library


*** Keywords ***
"${model}" with id "${id}" should have "${field}" "${value}"
    Check Admin Textfield    ${model}    ${id}    ${field}    ${value}

"${model}" with id "${id}" and email "${value}" should have "${field}"
    Check Admin Emailfield    ${model}    ${id}    ${field}    ${value}

"${model}" with id "${id}" should have image "${field}" "${value}"
    Check Image Is Added    ${model}    ${id}    ${field}    ${value}

"${model}" with id "${id}" should have as friend "${friends_name}"
    Check Friend Is Added   ${model}  ${id}  ${friends_name}

"User with id "${id}" should exist"
    Check User Exists  ${id}