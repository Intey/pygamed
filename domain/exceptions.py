class InitializationException(Exception):
    """
    Erorr that raised when initializing domain parts is wrong
    """
    def __init__(self, message, *args, **kwargs):
        Exception.__init__(self, message, *args, **kwargs)
        self.message = message
