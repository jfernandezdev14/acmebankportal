from werkzeug.exceptions import Unauthorized, NotFound, BadRequest, InternalServerError

class HttpUnauthorized(Unauthorized):
    """
    HttpUnauthorized class
    """
    def __init__(self, message=""):
        """
        HttpUnauthorized constructor
        :param message: String, message of the exception. Ie, "Unauthorized access"
        """
        Unauthorized.__init__(self)
        self.description = message


class HttpNotFound(NotFound):
    """
    HttpNotFound class
    """

    def __init__(self, message=""):
        """
        HttpNotFound constructor
        :param message: String, message of the exception. Ie, "Object not found"
        """
        HttpNotFound.__init__(self, message)
        self.description = message


class HttpBadRequest(BadRequest):
    """
    HttpBadRequest class
    """

    def __init__(self, message=""):
        """
        HttpBadRequest constructor
        :param message: String, message of the exception. Ie, "Bad request"
        """
        BadRequest.__init__(self, message)
        self.description = message


class HttpServerError(InternalServerError):
    """
    HttpServerError class
    """

    def __init__(self, message=""):
        """
        HttpServerError constructor
        :param message: String, message of the exception. Ie, "Internal server error"
        """
        InternalServerError.__init__(self, message)
        self.description = message
