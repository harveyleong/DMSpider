class DMException(Exception):
    '''Basic Exception of doggo.'''

    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return self.message


class RequestException(DMException):
    pass


class SearchException(DMException):
    pass
