import os
import requests
import json
import re

from asapis.services.baseServiceLib import BaseServiceLib
from asapis.utils.printUtil import out

class ASoC(BaseServiceLib):
    host = "https://cloud.appscan.com"
    apiVersion = "2"

    # authorization info exists after authorizing to ASoC
    authInfo = {}

    __httpMarker = re.compile("^http", re.IGNORECASE)

    # process the command-line options and performs the initial authorization with ASoC
    def __init__(self):
        super().__init__()
        self.host = self.Options["host"].lstrip("/") if self.Options["host"] else self.host
        self.apiVersion = self.Options["apiVersion"] if self.Options["apiVersion"] else self.apiVersion
        self.verifyHost()
        self.authorize()

    def verifyHost(self):
        try:
            self.get("")
        except:
            out(f"Failed connecting to {self.host}. Make sure host is valid and accessible.")
            exit(1)

    # get a session token using the Key ID and Secret
    # authorization header is stored for use in subsequent requests
    def authorize(self, keyId: str= None, keySecret: str= None): 
        if keyId is None:
            if not self.Options:
                self.getCommandLineOptions()
            if "asoc" in self.Options:
                keyId = self.Options["asoc"]["KeyId"]
                keySecret = self.Options["asoc"]["KeySecret"]
            else: 
                raise AssertionError('Options must contain "asoc" with "KeyId" and "KeySecret"')

        if not keyId or not keySecret:
            raise AssertionError("Credentials not supplied, can not authenticate. Check configuration file or provide credentials via command-line")

        loginObj = {"KeyId": keyId, "KeySecret": keySecret}

        url = f"{self.host}/api/V{self.apiVersion}/Account/ApiKeyLogin"

        self.applyConnectionConfig()

        res = self.session.post(url, json=loginObj)
        if not res.ok:
            self.printResponseError(res)
            exit(1)

        self.authInfo = res.json()
        self.session.headers.update({"Authorization": "Bearer " + self.authInfo["Token"]})

        self.getUserData()

        print(f"{self.host} authorized {self.authInfo['userName']} ({self.authInfo['email']}) at {self.authInfo['org']}")


    def applyConnectionConfig(self):
        if "cert" in self.Options:
            self.session.cert = self.Options["cert"]
            
        if "proxies" in self.Options:
            self.session.Verify = False
            self.session.proxies = json.loads(self.Options["proxies"])

    def getUserData(self):

        res = self.get("Account/TenantInfo")
        if not res.ok:
            return

        info = res.json()
        self.authInfo["userName"] = f"{info['UserInfo']['FirstName']} {info['UserInfo']['LastName']}"
        self.authInfo["email"] = info['UserInfo']["Email"]
        self.authInfo["org"] = info["TenantName"]

    def upload(self, filePath: str, **kwargs) -> requests.Response:
        """Upload a file to use in subsequence operation (execute a scan)
            Args:

                filePath: full path of the file to upload
                <requests args>: all requests.post arguments are accepted

            Returns:

                None if operation failed
                FileID of the created file if uploaded is successful
        """
        with open(filePath, "rb") as uploadedFile:
            files = {'fileToUpload': (os.path.basename(filePath), uploadedFile, "application/octet-stream") }
            res = self.post("FileUpload", files=files)
            if res.ok:
                uploadedFile = res.json()
                return uploadedFile["FileId"]
            else:
                self.printResponseError(res)

        return None

    def getAbsoluteUri(self, uri: str) -> str:
        """Prepends the host and api/version prefix to the partial API URI

            Args:

                uri: the partial API URI

            Returns:

                Fully qualified URI for the request                           
        """
        # this is for hard-coded hosts, in case it's preferred by the user
        # (http marker assumed to be the start of a fully qualified URI)
        if bool(self.__httpMarker.match(uri)):
            return uri

        uri = uri.lstrip("/")
        uri = f"{self.host}/api/v{self.apiVersion}/{uri}"
        return uri

    def getErrorMessage(self, response: requests.Response) -> str:
        """Returns a formatted message with ASoC data (when available)
        """
        try:
            errorData = response.json()
            formatParams = []
            numParams = 0
            if "formatParams" in errorData:
                formatParams = errorData["FormatParams"]
                numParams = range(len(formatParams))
            message = errorData["Message"]
            
            message = f"{message} - ASOCError:{errorData['Key']}"
            for i in range(numParams):
                placeholder = f"{{{i}}}"
                message = message.replace(placeholder, formatParams[i])
            return message
        except ValueError:
            return None


# Authorizes and outputs a session token. Part utility, part test.
if __name__ == "__main__":
    asoc = ASoC()
    print(f"Authorization token: {asoc.authInfo['Token']}")

