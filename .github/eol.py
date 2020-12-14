from course_discovery.settings.production import *

# Static serve
MIDDLEWARE += (
    'whitenoise.middleware.WhiteNoiseMiddleware',
)

# STATIC FILES SERVE 
# should be configured on the discovery.yml file
#STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
#STATIC_ROOT= '/edx/app/discovery/course_discovery/static'