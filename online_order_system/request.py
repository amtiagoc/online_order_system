class Request:
    def __init__(self, credentials, data, ipAddress):
        self.credentials = credentials
        self.data = data
        self.ipAddress = ipAddress

class RequestHandler:
    def __init__(self, successor=None):
        self.successor = successor

    def handleRequest(self):
        pass

    def setSuccessor(self, successor):
        self.successor = successor