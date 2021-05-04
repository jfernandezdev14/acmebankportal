import json
import os
from io import StringIO

from flask import request, redirect
from flask_restful import Resource
from werkzeug.utils import secure_filename

from app.controllers.acmebank_controller import AcmeBankController
from app.utilities.decorators.decorators import handle_api_exceptions


class AcmeBankProcessJsonResource(Resource):
    """
    Contains the list of methods exposed of the UsersResource
    """

    @handle_api_exceptions()
    def post(self):
        """
        Retrieves the information of an user
        :return:
        """
        if "json_file" in request.files:

            json_file = request.files['json_file'].read()
            data = json.loads(json_file)
            acmebank_controller = AcmeBankController(json_data=data)
            process_response = acmebank_controller.process_json()
            return process_response

        return redirect('/')
