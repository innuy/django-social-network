import os



SERVER = 'localhost:8001'
BROWSER = 'Chrome'
DELAY = 0
DEFAULT_USERNAME= 'Admin'
DEFAULT_PASSWORD= 'pass12345'
VALID_USER = 'demo'
VALID_PASSWORD =  'mode'
LOGIN_URL=     'http://${SERVER}/'
WELCOME_URL=    'http://${SERVER}/'
ERROR_URL=      'http://${SERVER}/error.html'
ADD_FRIEND_URL=   'http://${SERVER}/users/'
REGISTRATION_URL=   'http://${SERVER}/register/'
ADMIN_URL=      'http://${SERVER}/admin/socialNetworkApp'
USER_MODEL=     'user'
USERFRIEND_MODEL=  'userfriend'
FRIENDS_PAGE=   'http://${SERVER}/friends/'
EDIT_PAGE=    'http://${SERVER}/edit/'
IMAGE_FILE_XPATH=   '//div[@class="form-row field-profile_image"]//p[@class="file-upload"]//a'
PAGE_DELAY = 30