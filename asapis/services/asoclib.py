import os
from sys import api_version
import requests
import json
import re

from asapis.services.baseServiceLib import BaseServiceLib
from asapis.utils.printUtil import logger, print_result

class ASoC(BaseServiceLib):
    """
    Wraps basic operations to simplify interactions with AppScan on Cloud

    Once created, the object is ready to operate as it automatically initializes and authenticates. 
    """
    host = "https://cloud.appscan.com"
    api_version = "2"

    # authorization info exists after authorizing to ASoC
    auth_info = {}

    __http_marker = re.compile("^http", re.IGNORECASE)

    # process the command-line options and performs the initial authorization with ASoC
    def __init__(self):
        super().__init__()
        self.host = self.config["ASoC"]["Host"].rstrip("/") if self.config["ASoC"]["Host"] else self.host
        if "APIVersion" in self.config["ASoC"]:
            self.api_version = self.config["ASoC"]["APIVersion"]
        self.__verifyHost()
        self.authorize()

    def __verifyHost(self):
        """Verifies that the host is reachable"""
        try:
            requests.get(self.host)
        except:
            logger(f"Failed connecting to {self.host}. Make sure host is valid and accessible.")
            exit(1)

    # get a session token using the Key ID and Secret
    # authorization header is stored for use in subsequent requests
    def authorize(self, key_id: str= None, key_secret: str= None): 
        """Causes an ApiKeyLogin request with the provided credentials (or from the config).

           Once successful, the auth_info object is updated with the correct session token.
        """
        if key_id is None:
            if "ASoC" in self.config:
                key_id = self.config["ASoC"]["KeyId"]
                key_secret = self.config["ASoC"]["KeySecret"]
            else: 
                raise AssertionError('config must contain "asoc" with "KeyId" and "KeySecret"')

        if not key_id or not key_secret:
            raise AssertionError("Credentials not supplied, can not authenticate. Check configuration file or provide credentials via command-line")

        login_obj = {"KeyId": key_id, "KeySecret": key_secret}

        url = f"{self.host}/api/V{self.api_version}/Account/ApiKeyLogin"

        res = self.session.post(url, json=login_obj)
        if not res.ok:
            self.print_response_error(res)
            exit(1)

        self.auth_info = res.json()
        self.session.headers.update({"Authorization": "Bearer " + self.auth_info["Token"]})

        self.get_user_data()

        logger(f"{self.host} authorized {self.auth_info['userName']} ({self.auth_info['email']}) at {self.auth_info['org']}")

    def get_user_data(self):

        res = self.get("Account/TenantInfo")
        if not res.ok:
            return

        info = res.json()
        self.auth_info["userName"] = f"{info['UserInfo']['FirstName']} {info['UserInfo']['LastName']}"
        self.auth_info["email"] = info['UserInfo']["Email"]
        self.auth_info["org"] = info["TenantName"]

    def upload(self, file_path: str, **kwargs) -> requests.Response:
        """Upload a file to use in subsequence operation (execute a scan)
            Args:

                filePath: full path of the file to upload
                <requests args>: all requests.post arguments are accepted

            Returns:

                None if operation failed
                FileID of the created file if uploaded is successful
        """
        with open(file_path, "rb") as uploaded_file:
            files = {'fileToUpload': (os.path.basename(file_path), uploaded_file, "application/octet-stream") }
            res = self.post("FileUpload", files=files)
            if res.ok:
                uploaded_file = res.json()
                return uploaded_file["FileId"]
            else:
                self.print_response_error(res)

        return None

    def get_absolute_uri(self, uri: str) -> str:
        """Prepends the host and api/version prefix to the partial API URI

            Args:

                uri: the partial API URI

            Returns:

                Fully qualified URI for the request                           
        """
        # this is for hard-coded hosts, in case it's preferred by the user
        # (http marker assumed to be the start of a fully qualified URI)
        if bool(self.__http_marker.match(uri)):
            return uri

        uri = uri.lstrip("/")
        uri = f"{self.host}/api/v{self.api_version}/{uri}"
        return uri

    def get_error_message(self, response: requests.Response) -> str:
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

    def get_model(self, action:str)-> dict:
        """Retruns the correct version of the model according
        to the action that is wanted

        Arg:

        action: the name of the action (corresponds to the config item)

        Return:
            
            The model for the correct API version
        """
        return self.config[action][f"ModelV{api_version}"]

# Authorizes and outputs a session token. Part utility, part test.
if __name__ == "__main__":
    asoc = ASoC()
    print_result(f"Authorization token: {asoc.auth_info['Token']}")

