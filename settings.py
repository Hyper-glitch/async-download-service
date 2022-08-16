"""Module for setting vars."""
from environs import Env

env = Env()
env.read_env()

ENABLE_RESPONSE_DELAY = env.bool('ENABLE_RESPONSE_DELAY', False)
ENABLE_LOGGING = env.bool('ENABLE_LOGGING', False)
RESPONSE_DELAY = env.int('RESPONSE_DELAY', 0)
PHOTOS_DIR = env.str('PHOTOS_DIR', 'test_photos')
