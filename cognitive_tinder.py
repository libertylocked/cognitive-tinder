#!/usr/bin/env python
"""Run profile photos through MS cognitive services"""
import webbrowser
import fb_auth
import requests
import config_keys

_CV_URL = 'https://westus.api.cognitive.microsoft.com/vision/v1.0/describe?maxCandidates=1'
#_EMOTION_URL = 'https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize'

def main():
    """Main function"""
    # this will only work if user has generated the token file
    session = fb_auth.create_tinder_session()
    while True:
        loop(session)

def loop(session):
    """Runs through recommended users and run their photos thru cog services"""
    nearby = session.nearby_users()
    for hopeful in nearby:
        print '==============================='
        # print user id
        print hopeful.id
        # filter rules
        if should_skip_profile(hopeful):
            print 'Skipped', hopeful.name
            continue
        # print hopeful's info
        print 'Name:', hopeful.name
        print 'Age:', hopeful.age
        print 'Schools:', hopeful.schools
        print 'Jobs:', hopeful.jobs
        print 'Bio:', hopeful.bio
        # send a post request to CV API
        for photo_url in hopeful.photos:
            print ' '
            print photo_url
            print get_cv_caption(photo_url)
        # let user swipe
        while True:
            swipe = raw_input('swipe y/n/s/b: ')
            if swipe == 'y':
                hopeful.like()
                break
            elif swipe == 'n':
                hopeful.dislike()
                break
            elif swipe == 's':
                hopeful.superlike()
                break
            elif swipe == 'b':
                for photo_url in hopeful.photos:
                    webbrowser.open(photo_url)

def should_skip_profile(hopeful):
    """Additional profile filter rules"""
    # modify if needed
    if hopeful.age > 100:
        return True
    return False

def get_cv_caption(url):
    """Gets the CV caption in JSON"""
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': config_keys.CV_KEY
    }
    json_data = {
        'url': url
    }
    response = requests.post(_CV_URL, json=json_data, headers=headers)
    return response.json()['description']['captions']

if __name__ == "__main__":
    main()
