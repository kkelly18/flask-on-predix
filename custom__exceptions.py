class ServiceBindingError(Exception):
    """Exception raised for errors binding to a service

    Attributes:
        vcap_services -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, vcap_services, message):
        self.expression = vcap_services
        self.message = message

