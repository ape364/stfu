from os import getenv

from dotenv import load_dotenv

load_dotenv(verbose=True)

API_TOKEN = getenv('API_TOKEN')
DEBUG = getenv('DEBUG', False)
