from os import environ
from pathlib import Path
from re import match

auth_creds_file = str(Path(__file__).parent.resolve()) + r'/creds.json'
POSTGRES_PASSWORD = environ['POSTGRES_PASSWORD']
POSTGRES_HOST = environ['POSTGRES_HOST']
POSTGRES_URI = f'postgresql://postgres:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/postgres'

BOT_TOKEN = environ['BOT_TOKEN']
ADMINS = environ['ADMINS'].split(',')

MAILING_TIME = environ['MAILING_TIME']
FROM_TABLE = environ['FROM_TABLE']
TO_TABLE = environ['TO_TABLE']
if not match(r'^([0-1]?\d|2[0-3]):[0-5]\d$', MAILING_TIME):
    raise ValueError("MAILING_TIME must be in HH:MM format")
