from .base import *
load_env()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', '(hw1@=f!)j)yh9$7hvnwfc1bp2#!b4ba@zs#3j$xn)crbefcux')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', True)
