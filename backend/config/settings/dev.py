"""

Local development Django settings for dhmit/paris_1970

Under no circumstances run the server with these settings in production!

"""

from .base import *  # pylint: disable=unused-wildcard-import, wildcard-import

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qqucn931x78rx054n(6g(s_3vxppjw$f24e(9&v6rsbd0&0$2e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SITE_ID = 1

ALLOWED_HOSTS = []  # wildcard

LANGUAGES = [
    ('en', 'English'),
    ('fr', 'French'),
]
