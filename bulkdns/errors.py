
class BulkDnsError(Exception):
    def __init__(self, message='BulkDnsError', code=0, error_chain=None):
        self.code = code
        self.message = message

    def __int__(self):
        """ integer value for errors"""
        return int(self.code)

    def __str__(self):
        """ string value for errors"""
        return str(self.message)


class BulkDnsApiError(BulkDnsError):
    """ API error, should be raised in case of api error in provider """
