Flask-Login-Oauth2
==================

Installation
-------
$ pip install -r requirements.txt


flask-login-oauth2 and google oauth2 library for authenticating users through New Google Oauth2 mechanism and maintaining session for users

Just register your new Google app at https://code.google.com/apis/console#access
and copy `settings-sample.py` to `settings.py` and modifiy `GOOGLE_CLIENT_ID` , `GOOGLE_CLIENT_SECRET`,
`REDIRECT_URI` and `SECRET_KEY`


run the server

    $python server.py
    Running on http://127.0.0.1:5000/

Register a new user also login in if the user exists
http://127.0.0.1:5000/login?email=anurag@grexit.com

It uses the following scopes:

    https://mail.google.com/

To Get all Access to the Gmail Imap server of the user

    https://www.googleapis.com/auth/userinfo.profile

To Get Access to the User Profile

Read More About Scopes here at https://developers.google.com/gdata/faq#AuthScopes

It also saves the accesstoken which can be used to get userinfo

GET https://www.googleapis.com/oauth2/v1/userinfo?access_token={accessToken}

To Logout
http://127.0.0.1:5000/logout

Flask-Login Reference
---------------------
http://packages.python.org/Flask-Login/

Google Oauth2 Library Reference
-------------------------------

https://developers.google.com/accounts/docs/OAuth2Login

https://developers.google.com/api-client-library/python/guide/aaa_oauth

