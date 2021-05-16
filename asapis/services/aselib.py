from http import HTTPStatus
import requests
import re
import urllib3

from requests.exceptions import SSLError

from asapis.services.baseServiceLib import BaseServiceLib
from asapis.utils.printUtil import logger, PrintLevel, print_result
from asapis.services.aseInventory import ASEInventory

class ASE(BaseServiceLib):
    """
    Wraps basic operations to simplify interactions with AppScan Enterprize

    Once created, the object is ready to operate as it automatically initializes and authenticates. 
    """
    host = ""
    instance = ""
    # authorization info exists after authorizing to ASE
    auth_info = {}

    inventory = ASEInventory()

    __http_marker = re.compile("^http", re.IGNORECASE)

    # process the command-line options and performs the initial authorization with ASE
    def __init__(self):
        super().__init__()
        self.__verifyHost()
        self.authorize()
        self.inventory.load(self)

    def __verifyHost(self):
        """Verifies that the host is reachable"""
        if "Host" not in self.config["ASE"]: 
            logger("\"Host\" is missing - ASE options must contain the ASE server host name")
            exit(1)
        self.host = self.config["ASE"]["Host"].rstrip("/")
        verify = self.config["ASE"]["Verify"] if "Verify" in self.config["ASE"] else True
        
        # If use explicitly set Verify=False to allow insecure requests, we surpress the warning
        if not verify:
            logger("Connection Verficiation Disabled. Disabling urllib3.exceptions.InsecureRequestWarning warning.", level=PrintLevel.Verbose)
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        else: logger("Connection Verficiation Enabled", level=PrintLevel.Verbose)

        self.session.verify = verify

        try:
            self.session.get(self.host)
        except SSLError:
            logger(f"SSL Error: Certificate Verification Error. Set ASE.Verify=False to connect to a server using a self-signed certificate.")
            exit(1)
        except Exception:
            logger(f"Failed connecting to {self.host}. Make sure host is valid and accessible.")
            exit(1)

        self.instance = self.host + "/" + self.config["ASE"]["Instance"]
        res = self.get(self.instance)
        if not res.ok:
            logger(f"Failed to find instance '{self.instance}'. Make sure the correct instance name is set in the onfig.")
            self.print_response_error_and_exit(res)

    def authorize(self):
        api_keys = True
        # if we have a KeyId and it's not empty, we prefer the ID/Secret combination
        if ("KeyId" in self.config["ASE"] and self.config["ASE"]["KeyId"]):
            key_id = self.config["ASE"]["KeyId"]
            key_secret = self.config["ASE"]["KeySecret"]
            logger(f"Opting to use API Key", level=PrintLevel.Verbose)
        else:
            key_id = self.config["ASE"]["Username"]
            key_secret = self.config["ASE"]["Password"]
            api_keys = False
            logger(f"Opting to use user credentials: ({key_id} - {key_secret})", level=PrintLevel.Verbose)

        if (api_keys):
            login_obj = {"keyId": key_id, "keySecret": key_secret}
            logger(f"API Key login: ({login_obj})", level=PrintLevel.Verbose)
            res = self.session.post(f"{self.instance}/api/keylogin/apikeylogin", json=login_obj, verify=self.session.verify)
            if not res.ok:
                logger("Failed authenticate using API Key.")
                self.print_response_error_and_exit(res)
            self.auth_info = res.json()
        else:
            login_obj = {"userId": key_id, "password": key_secret, "featureKey": "AppScanEnterpriseUser"}
            logger(f"User credentials login: ({login_obj})", level=PrintLevel.Verbose)
            res = self.session.post(f"{self.instance}/api/login", json=login_obj, verify=self.session.verify)
            if not res.ok:
                logger("Failed authenticate using user credentials.")
                self.print_response_error_and_exit(res)
            self.auth_info = res.json()

        self.session.headers.update({"asc_xsrf_token": self.auth_info["sessionId"]})
        self.session.cookies.update(res.cookies)

        self.get_user_data()

        logger(f"{self.instance} authorized {self.auth_info['userName']} ({self.auth_info['email']})")
        
    def get_user_data(self):

        res = self.get("currentuser_v2")
        if not res.ok:
            return

        info = res.json()
        self.auth_info["userName"] = info["fullName"]
        self.auth_info["email"] = info["email"]

    # Constructs a fully-qualified URI from the partial service API URI
    def get_absolute_uri(self, uri: str) -> str:
        """Prepends the right host and api/version prefix to the partial API URI

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
        uri = f"{self.instance}/api/{uri}"
        return uri

    def get_error_message(self, response: requests.Response) -> str:
        try:
            errorData = response.json()
            return errorData["errorMessage"]
        except ValueError:
            return None


# Authorizes and outputs a session token. Part utility, part test.
if __name__ == "__main__":
    ase = ASE()
    print_result(f"Session ID: {ase.auth_info['sessionId']}")
    cookies = ase.session.cookies.get_dict()
    print_result("Cookies:")
    for key in cookies:
        print_result(f"{key} = {cookies[key]}")

