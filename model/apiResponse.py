class ApiResponse:
    def __init__(self, status, body, message):
        self.status = status
        self.body = body
        self.message = message
        return self