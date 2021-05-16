import codecs
import json
import sys
from typing import Callable
import requests
from http import HTTPStatus
from abc import ABC, abstractmethod

from requests.api import request

from asapis.utils.configuration import Configuration
from asapis.utils.printUtil import logger, PrintLevel

class BaseServiceLib(ABC):

    # Processes the command-line options
    def __init__(self):
        # Holds the execution options
        # The only mandatory fields are the credentials needs to authenticate and authorize
        self.__configuration = Configuration(sys.argv[1:])
        # The one and only session be used in calling the APIs
        # Implemented classes should populate with required cookies and headers
        self.session = requests.Session()
        self.__apply_connection_config()

    @property
    def config(self):
        return self.__configuration.config

    def __apply_connection_config(self):
        if "cert" in self.config:
            self.session.cert = self.config["cert"]
            
        if "proxies" in self.config:
            self.session.Verify = False
            self.session.proxies = self.config["proxies"]

    # Called to update the session tokens required by the service
    @abstractmethod
    def authorize(self, keyId: str= None, keySecret: str= None) -> dict: 
        pass

    # Constructs a fully-qualified URI from the partial service API URI
    @abstractmethod
    def get_absolute_uri(self, uri: str) -> str:
        """Prepends the right host and api/version prefix to the partial API URI

            Args:

                uri: the partial API URI

            Returns:

                Fully qualified URI for the request
        """
        pass

    # Performs a GET operation, authorizing if needed
    def get(self, uri: str, **kwargs) -> requests.Response:
        """Sendan authenticated GET request to the server

            Args:

            uri: relative path after the API prefix (base API URL)\n
            <requests args>: all requests.post arguments are accepted

            Returns:
                
                The resulting response object of the call
        """
        get = lambda uri,**kwargs: self.session.get(uri, **kwargs)
        res = self.__internal_call("GET", get, uri, **kwargs)
        return res

    # Performs a POST operation, authorizing if needed
    def post(self, uri: str, **kwargs) -> requests.Response:
        """Sends an authenticated POST request to the server

            Args:

            uri-> relative path after the API prefix (base API URL)
            <requests args>: all requests.post arguments are accepted

            Returns:
                The resulting response object of the call
        """
        post = lambda uri,**kwargs: self.session.post(uri, **kwargs)
        res = self.__internal_call("POST", post, uri, **kwargs)
        return res

    # Performs a PUT operation, authorizing if needed
    def put(self, uri: str, **kwargs) -> requests.Response:
        """Sends an authenticated PUT request to the server

            Args:

            uri: relative path after the API prefix (base API URL)
            <requests args>: all requests.put arguments are accepted

            Returns:
                The resulting response object of the call
        """
        put = lambda uri,**kwargs: self.session.put(uri, **kwargs)
        res = self.__internal_call("PUT", put, uri, **kwargs)
        return res

    # performs a DELETE operation, authorizing if needed
    def delete(self, uri: str, **kwargs) -> requests.Response:
        """Sends an authenticated DELETE request to the server

            Args:

            uri: relative path after the API prefix (base API URL)
            <requests args>: all requests.delete arguments are accepted

            Returns:
                The resulting response object of the call
        """
        delete = lambda uri, **kwargs: self.session.delete(uri, **kwargs)
        res = self.__internal_call("DELETE", delete, uri, **kwargs)
        return res

    def download(self, uri: str, file_path: str, encoding:str = "binary", **kwargs):
        logger(f"Downloading file {uri} to {file_path} using {encoding} encoding",level=PrintLevel.Verbose)
        res = self.get(uri, stream=True)

        if not res.ok:
            self.print_response_error_and_exit(res)

        if encoding is "binary":
            with open(file_path, 'wb') as fd:
                for chunk in res.iter_content(chunk_size=1024):
                    fd.write(chunk)
        else:
            with codecs.open(file_path, "w", encoding) as fd:
                fd.write(res.text)

    # Executes the actual HTTP request using the provided operation function
    # the method is only needed for logging purposes, the actual call is done via the httpMathodCall lambda
    def __internal_call(self, method: str, httpMethodCall: Callable[[str,dict], requests.Response], uri: str, **kwargs) -> requests.Response:
        """Sends an authenticated request to the server. This method makes sure the absolute URI is used
            as well as re-authorizes in case of a 401 response.

            Args:

            method: the name of the HTTP method to call for logging purposes only
            httpMethodCall: a lambda function that performs the actual HTTP call
            uri: relative path after the API prefix (base API URL)
            <requests args>: all requests.delete arguments are accepted

            Returns:
                The resulting response object of the call
        """
        uri = self.get_absolute_uri(uri)

        logger(f"Initiating {method} request to {uri}",level=PrintLevel.Verbose)

        res = httpMethodCall(uri, **kwargs)
        if res.status_code == 401:
            logger("Response is 401 Unauthorized, authorizing and retrying", level=PrintLevel.Verbose)
            self.authorize()
            res = httpMethodCall(uri, **kwargs)

        return res

    # Prints the formatted response error to output
    def print_response_error(self, response: requests.Response) -> None:
        """Prints the details of an error response. The code and message (if available).
        Message is formatted by implementing the abstract getErrorMessage method

            Args:

                response: the response returned from the server.
        """
        message = self.get_error_message(response)
        code = self.get_respond_code_text(response)
        if message:
            logger(f"ASoC Error: {code.value} {code} - {message}")
        else:
            logger(f"ASoC Error: {code.value} {code.name}")

    # Prints the formatted response error to output and exit
    def print_response_error_and_exit(self, response: requests.Response) -> None:
        """Prints the details of an error response. The code and message (if available).
        Message is formatted by implementing the abstract getErrorMessage method

            Args:

                response: the response returned from the server.
        """
        self.print_response_error(response)
        exit(1)

    
    @abstractmethod
    def get_error_message(self, response: requests.Response) -> str:
        return response.text

    def get_respond_code_text(self, response: requests.Response) -> HTTPStatus:
        try:
            return HTTPStatus(response.status_code)
        except ValueError:
            return response.status_code

