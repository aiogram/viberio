from aiohttp import ClientResponse


class ViberApiException(Exception):
    def __init__(self, response: ClientResponse, message: str, payload: dict):
        self.response = response
        self.message = message
        self.payload = payload

        self.status = response.status
        self.path = response.url.path

    def __str__(self):
        return f"failed to post request to endpoint={self.path}, with payload={self}. error is: {self.message}"


class ViberException(Exception):
    def __init__(self, message, status, obj):
        self.message = message
        self.status = status
        self.obj = obj

    def __str__(self):
        return f"request failed with status {self.status}, message: {self.message}"

    @classmethod
    def check(cls, result: dict):
        if result.get('status') != 0:
            raise cls(result['status_message'], result['status'], result)
        return True
