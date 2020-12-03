import requests
from http import HTTPStatus

from baseServiceLib import BaseServiceLib

class ASoC(BaseServiceLib):
    # authorization info exists after authorizing to ASoC
    authInfo = {}
    authHeaders = {}

    # process the command-line options and performs the initial authorization with ASoC
    def __init__(self):
        
        super().__init__()
        self.authorize()

    # get a session token using the Key ID and Secret
    # authorization header is stored for use in subsequent requests
    def authorize(self, keyId=None, keySecret=None):
        if keyId is None:
            if not self.Options:
                self.getCommandLineOptions()
            if "asoc" in self.Options:
                keyId = self.Options["asoc"]["KeyId"]
                keySecret = self.Options["asoc"]["KeySecret"]
            else: 
                raise AssertionError('Options must contain "asoc" with "KeyId" and "KeySecrect"')

        loginObj = {"KeyId": keyId,  "KeySecret": keySecret}

        res = requests.post("https://cloud.appscan.com/api/V2/Account/ApiKeyLogin", json=loginObj)
        if res.status_code != 200:
            print(res.text)

        self.authInfo = res.json()

        self.authHeaders = {"Authorization": "Bearer " + self.authInfo["Token"]}

        return self.authHeaders

    # performs a GET operation, authorizing if needed
    def get(self, uri, **kwargs):
        if not self.authInfo:
            self.authorize()

        self.addAuthHeaders(kwargs)

        res = requests.get(uri, **kwargs)
        if res.status_code == 401:
            self.authorize()
            self.addAuthHeaders(kwargs)
            res = requests.get(uri, **kwargs)

        if res.status_code != 200:
            print(res.text)

        return res

    # performs a POST operation, authorizing if needed
    def post(self, uri, **kwargs):
        if not self.authInfo:
            self.authorize()

        self.addAuthHeaders(kwargs)

        res = requests.post(uri, **kwargs)
        if res.status_code == 401:
            self.authorize()
            self.addAuthHeaders(kwargs)
            res = requests.post(uri, **kwargs)

        if not res.ok:
            print(res.text)

        return res

    # adds the authorization header to the request. If a "headers" key exists in the request object, the auth headers
    # are added. If "headers" do not exist the auth headers are set as with "headers" key
    def addAuthHeaders(self, reqArgs):
        if "headers" in reqArgs:
            reqArgs["headers"].update(self.authHeaders)
        else:
            reqArgs["headers"] = self.authHeaders

    def printResponseError(self, response):
        message = self.getErrorMessage(response)
        code = self.getRespondCodeText(response)
        if message:
            print(f"ASoC Error: {code} - {message}")
        else:
            print(f"ASoC Error: {code}")

    def getErrorMessage(self, response):
        try:
            errorData = response.json()
            formatParams = errorData["formatParams"]
            numParams = range(len(formatParams))
            message = errorData["message"]
            for i in numParams:
                placeholder = f"{{{i}}}"
                message = message.replace(placeholder, formatParams[i])
            return message
        except ValueError:
            return None

    def getRespondCodeText(self, response):
        try:
            return HTTPStatus(response.status_code)
        except ValueError:
            return response.status_code
