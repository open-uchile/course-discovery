from course_discovery.settings.production import *

# Static serve
MIDDLEWARE += (
    'whitenoise.middleware.WhiteNoiseMiddleware',
)
