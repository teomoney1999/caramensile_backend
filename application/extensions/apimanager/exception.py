from werkzeug.exceptions import *

class ValidationError(HTTPException):
    """Raised when there is a problem deserializing a dictionary into an
    instance of a SQLAlchemy model.

    """
    pass