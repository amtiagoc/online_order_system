class OrderManager:
    def __init__(self, requestHandler):
        self.requestHandler = requestHandler

    def processRequest(self, request):
        self.requestHandler.handleRequest(request)
        print("The process has been completed successfully")