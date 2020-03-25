class Error(Exception):
   """Base class for other exceptions"""
   pass

class ValueTooSmallError(Error):
   """Raised when the input value is too small"""
   pass

class ValueTooLargeError(Error):
   """Raised when the input value is too large"""
   pass

class ParseSequenceError(Error):
    """There is something wrong during the parse sequence"""
    pass


class UnSupportedElfFormatError(Error):
    """this kind of debug structure information is not supported for now"""
    pass

   