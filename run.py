#!flask/bin/python
from flask_restful import Api

from app import app
from app.resources.acmebank_resources import AcmeBankProcessJsonResource

acmebankportal_api = Api(app)

# List of Endpoints

acmebankportal_api.add_resource(
    AcmeBankProcessJsonResource,
    '/process-json'
)


@app.route('/')
def index():
    return '''
        <h1>Process file</h1>
        <form method="POST" action="/process-json" enctype="multipart/form-data">
            <label for="name">Upload your Json File</label>
            <input type="file" name="json_file"><br><br>
            <input type="submit">
        </form>
    '''


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
