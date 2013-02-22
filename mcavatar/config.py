#===============================#
# Flask config                  #
#===============================#

# This is set so that Flask is
# able to figure out the subdomains
SERVER_NAME = 'mcavatar.dev:5000'

# Number in seconds to keep images
# alive in redis (Default = 24 hours)
IMG_CACHE_TIMEOUT = 60 * 60 * 24

DEFAULT_IMG_SIZE = 48
MAX_IMG_SIZE = 250
LOW_IMG_SIZE = 16

#===============================#
# Redis config                  #
#===============================#

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 7  # Must be an integer
