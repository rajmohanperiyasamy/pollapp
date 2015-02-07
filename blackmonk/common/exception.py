class AppException(Exception):
    def __init__(self, error_message,error_code=None):
        self.message = error_message
        self.code = error_code
    def __str__(self):
        return repr(self.parameter)