#! /usr/bin/env python
#! -*- coding: utf-8 -*-
# This Library combines Google Oauth and User management 

import json
import requests
from flask import Flask, request, redirect
from flask.ext.login import (LoginManager, current_user, login_required,
                             login_user, logout_user, UserMixin, AnonymousUserMixin)


app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('settings.py')

# User base class
class User(UserMixin):
    """User Session management Class
    """
    def __init__(self, email, id, fname="", lname="", accesstoken="", active=True):
        self.email = email
        self.id = id
        self.active = active
        self.fname = fname
        self.lname = lname
        self.accesstoken = accesstoken

    def is_active(self):
        return self.active

    def myemail(self):
        return self.email

    def get_userid(self):
        return self.id

    def get_fname(self):
        return self.fname

    def get_lname(self):
        return self.lname

"""
USER_STORE is the store of all the users. Ideally it should be in Database
"""
USERS = {
    1: User("anurag@grexit.com", 1, "Anurag", "Maher", "", True)
}

"""
USER_NAMES maintains a dictionary of all the users with their email address
"""
USER_NAMES = dict((u.email, u) for u in USERS.itervalues())


class Anonymous(AnonymousUserMixin):
    name = u"Anonymous"


@app.route("/")
def hello():
    if current_user.is_authenticated():
        return " User " + str(current_user.myemail()) + " is logged in "

    return "Hello World!"


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    from modules.oauth2 import GeneratePermissionUrl
    if current_user.is_authenticated():
        return current_user.get_id()

    if request.method == "GET":
        useremail = request.args.get('email', '')
        if useremail:
            if useremail in USER_NAMES:
                loginit = login_user(USER_NAMES[useremail], remember="yes")
                return "user already exists and logged in"

    if request.method == "GET" and request.args.get('email', ''):
        url = GeneratePermissionUrl(app.config['GOOGLE_CLIENT_ID'], request.args.get('email', ''),
            redirect_uri=app.config['REDIRECT_URI'], google_account_base_url=app.config['GOOGLE_ACCOUNTS_BASE_URL'])
        return redirect(url)
    return "No Email Provided"


@app.route("/oauth2callback", methods=["GET", "POST"])
def oauth2callback():
    from grexit.modules.imap.oauth2 import AuthorizeTokens
    if request.method == "GET":
        authorizationcode = request.args.get('code', '')
        useremail = request.args.get('state', '')
        response = AuthorizeTokens(app.config['GOOGLE_CLIENT_ID'],
                                   app.config['GOOGLE_CLIENT_SECRET'],
                                   authorizationcode,
                                   redirect_uri=app.config['REDIRECT_URI'],
                                   google_account_base_url=app.config['GOOGLE_ACCOUNTS_BASE_URL'])
        accesstoken = response["access_token"]
        r = requests.get('https://www.googleapis.com/oauth2/v1/userinfo?access_token=' + accesstoken)
        j = json.loads(r.text)
        if useremail != j["email"]:
            return "Initiated e-mail does not match with the authenticated email"
        options = {}
        options["email"] = j.get("email")
        options["firstname"] = j.get("given_name")
        options["lastname"] = j.get("family_name")
        options["accesstoken"] = accesstoken
        userid = options['userid']
        u = User(options.get("email"), userid, options.get("firstname"), options.get("lastname"), accesstoken)
        USERS[userid] = u
        loginit = login_user(u, remember="yes")
        if loginit == True:
            return "Everything happened Successfullly"
        return "Some Problem happened"
    else:
        return "Ony POST requests are allowed"                                 

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.anonymous_user = Anonymous


@login_manager.user_loader
def load_user(id):
    return USERS.get(int(id))

if __name__ == "__main__":
    app.run(debug=True)
