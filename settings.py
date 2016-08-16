'''
Settings based on dec_base defaults::

    Copyright (C) 2011 Department of Environment & Conservation

    Authors:
     * Adon Metcalfe
     * Dale Smith

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''

# Standard DEC settings template imported from dec_base
# pulls settings from dec_base/settings.py and dec_base/authentication.py
from dec_base import defaults; defaults()

'''
----------------------------
Custom settings beneath here
----------------------------
'''
DEBUG = True if os.environ.get('DEBUG', False) == 'True' else False
# Aviation application version number
APPLICATION_VERSION_NO = '15.10.0'

# Application title
SITE_TITLE = 'Aviation System'

# Database configuration
import dj_database_url, os
DATABASES = {
    # Defined in DATABASE_URL env variable.
    'default': dj_database_url.config(),
}

if not DEBUG:
    # Localhost, UAT and Production hosts
    ALLOWED_HOSTS = [
        'localhost',
        '127.0.0.1',
        'aws-oim-001',
        'aviation.dpaw.wa.gov.au',
        'aviation.dpaw.wa.gov.au.',
        'aviation-uat.dpaw.wa.gov.au',
        'aviation-uat.dpaw.wa.gov.au.',
    ]

SECRET_KEY = os.environ['SECRET_KEY'] if os.environ.get('SECRET_KEY', False) else 'foo'

INSTALLED_APPS += (
    'django_wsgiserver',
    'avs',
)

# Defines whether anonymous users have access to any views (via restless middleware)
ALLOW_ANONYMOUS_ACCESS = False
# List of URLs that are exempted from the above rule
LOGIN_EXEMPT_URLS = []

# Add a context to all templates
def global_template_context(request):
    return {'sitetitle':"Aviation System",
            'application_version_no':"15.10",
            'application_custodian':"Fire Management Services",
            'production_site': not DEBUG,
            }

TEMPLATE_CONTEXT_PROCESSORS += ("settings.global_template_context",)
