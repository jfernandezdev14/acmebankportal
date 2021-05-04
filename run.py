#!flask/bin/python
from app import app
from app.api import configure_endpoints

configure_endpoints(app)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
