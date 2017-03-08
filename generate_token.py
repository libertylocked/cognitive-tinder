#!/usr/bin/env python
"""Program to generate facebook auth token for Tinder"""
import fb_auth

def main():
    """Generates token file by logging in"""
    print "To generate a login token, we need your facebook credentials"
    email, password = fb_auth.get_fb_credentials_from_input()
    print "Acquiring token..."
    token = fb_auth.get_fb_access_token(email, password)
    print "Saving to token.txt..."
    fb_auth.save_access_token_to_file(token)
    print "Done"

if __name__ == "__main__":
    main()
