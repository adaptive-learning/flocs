"""
Private settings that should not be uploaded to GitHub or published in any way.
This file keeps secret keys for OAuth(2) providers and Django as well.
"""

# Django secret key used for session hashes and cryptography inside Django
SECRET_KEY = '-zocq!_l$gw_@cc1u7l$7j8y=b&+t2e4^e9bmx1&rk0ztp*&dj'

# registered Google application ID
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'your google key'
# registered Google application secret
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'your google secret'

# registered Facebook application ID
SOCIAL_AUTH_FACEBOOK_KEY = 'your facebook key'
# registered Facebook application secret
SOCIAL_AUTH_FACEBOOK_SECRET = 'your facebook secret'
