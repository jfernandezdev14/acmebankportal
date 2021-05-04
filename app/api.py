#!flask/bin/python
from flask_restful import Api
from app.resources.acmebank_resources import AcmeBankProcessJsonResource


def configure_endpoints(app):
    """
    Defines the list of endpoints of the application
    :param app: Flask App
    """
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
