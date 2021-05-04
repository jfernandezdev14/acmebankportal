from os import environ

from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# Base services urls
FS_API_URL_V1 = environ.get("FS_API_URL_V1") or 'http://localhost:8001/financialservice/api/v1.0'
US_API_URL_V1 = environ.get("US_API_URL_V1") or 'http://localhost:8002/userservice/api/v1.0'

# Userservice Endpoint urls
VALIDATE_USER_API_URL = US_API_URL_V1 + '/validate-user'

# Financialservice Endpoint urls
BANK_ACCOUNT_API_URL = FS_API_URL_V1 + '/accounts'

