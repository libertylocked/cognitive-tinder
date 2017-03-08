"""Facebook auth helper"""
import getpass
import os
import re
import requests
import pynder

import robobrowser

MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; U; en-gb; KFTHWI Build/JDQ39) \
AppleWebKit/535.19 (KHTML, like Gecko) Silk/3.16 Safari/535.19"
FB_AUTH_URL = "https://www.facebook.com/v2.6/dialog/oauth?redirect_uri=fb464891386855067%3A\
%2F%2Fauthorize%2F&display=touch&state=%7B%22challenge%22%3A%22IUUkEUqIGud332lfu%252BMJhxL4\
Wlc%253D%22%2C%220_auth_logger_id%22%3A%2230F06532-A1B9-4B10-BB28-B29956C71AB1%22%2C%22com.\
facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D&scope=user_birthd\
ay%2Cuser_photos%2Cuser_education_history%2Cemail%2Cuser_relationship_details%2Cuser_friend\
s%2Cuser_work_history%2Cuser_likes&response_type=token%2Csigned_request&default_audience=fr\
iends&return_scopes=true&auth_type=rerequest&client_id=464891386855067&ret=login&sdk=ios&lo\
gger_id=30F06532-A1B9-4B10-BB28-B29956C71AB1&ext=1470840777&hash=AeZqkIcf-NEW6vBd"
TOKEN_FILE = "token.txt"

def get_fb_access_token(email, password):
    """Gets FB access token by email and password"""
    browser = robobrowser.RoboBrowser(user_agent=MOBILE_USER_AGENT, parser="lxml")
    browser.open(FB_AUTH_URL)
    # submit login form
    login_form = browser.get_form()
    login_form["pass"] = password
    login_form["email"] = email
    browser.submit_form(login_form)
    # click the 'ok' button on the dialog informing you that you
    # have already authenticated with the Tinder app
    confirm_form = browser.get_form()
    browser.submit_form(confirm_form, submit=confirm_form.submit_fields['__CONFIRM__'])
    # get access token from the html response
    access_token = re.search(r"access_token=([\w\d]+)",
                             browser.response.content.decode()).groups()[0]
    return access_token

def get_fb_access_token_from_file():
    """Reads FB token from file"""
    if not os.path.isfile(TOKEN_FILE):
        return None
    with open(TOKEN_FILE, 'r') as token_file:
        token = token_file.read()
    return token

def get_fb_credentials_from_input():
    """Gets FB credientials from prompt"""
    email = getpass.getpass("Enter FB email: ")
    password = getpass.getpass("Enter FB password: ")
    return email, password

def save_access_token_to_file(token):
    """Writes the facebook auth token to file"""
    with open(TOKEN_FILE, 'w') as token_file:
        token_file.write(token)

def delete_access_token_file():
    """Deletes saved token file"""
    if os.path.isfile(TOKEN_FILE):
        os.remove(TOKEN_FILE)

def get_fb_id(access_token):
    """Gets facebook ID from access token"""
    req = requests.get('https://graph.facebook.com/me?access_token=' + access_token)
    return req.json()["id"]

def create_tinder_session():
    """Creates a tinder session.
    Only works if token file is generated!"""
    token = get_fb_access_token_from_file()
    if token != None:
        fb_id = get_fb_id(token)
        return pynder.Session(fb_id, token)
    else:
        raise Exception("No token file. Run generate_token.py first")
    