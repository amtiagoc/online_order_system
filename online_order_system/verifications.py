from request import RequestHandler
import json

class CacheManager(RequestHandler):
    def __init__(self, successor=None):
        super().__init__(successor)

    def cacheOperation(self, request):
        # The available cache operations using the order manager.
        registered = False
        print("Checking if the order is already registered...")
        with open("orders.txt", "r") as file:
            for line in file:
                if line.strip() == request.data.order:
                    registered = True
                    break
        if registered:
            print("The order is already registered, it will be sent to the order manager")
        else:
            with open("orders.txt", "a") as file:
                file.write(request.data.order + "\n")
            print("The order is not registered, it will be sent to the order manager")

    def handleRequest(self, request):
        self.cacheOperation(request)
        if self.successor is not None:
            self.successor.handleRequest(request)


class DataSanitizer(RequestHandler):
    def __init__(self, successor=None, json_data=None):
        super().__init__(successor)
        self.json_data = json_data

    def sanitizeData(self):
        # Sanitize the json data received.
        print("Sanitizing the data of the order",self.json_data['order'])
        return json.dumps(self.json_data['order'])

    def handleRequest(self, request):
        self.sanitizeData()
        if self.successor is not None:
            self.successor.handleRequest(request)

class RequestFilter(RequestHandler):
    def __init__(self, successor=None, role_permissions=None, ip_address=None):
        super().__init__(successor)
        self.role_permissions = role_permissions
        self.ip_address = ip_address

    def filterRequests(self):
        # Lógica de filtrado de solicitudes
        print("Filter by ip adress to check if it is in the blacklist...")
        with open("blacklist.txt", "r") as file:
            for line in file:
                if line.strip() == self.ip_address:
                    print("You are blacklisted from this system, talk to the administrator")
                    exit()

    def handleRequest(self, request):
        self.filterRequests()
        if self.successor is not None:
            self.successor.handleRequest(request)
