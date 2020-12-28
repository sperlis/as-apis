import sys
from typing import Callable
import requests
from http import HTTPStatus
from abc import ABC, abstractmethod

from asapis.utils.execOptions import OptionsProcessor
from asapis.utils.printUtil import out

class BaseServiceLib(ABC):

    # Holds the execution options
    # The only mandatory fields are the credentials needs to authenticate and authorize
    Options = {}

    # The one and only session be used in calling the APIs
    # Implemented classes should populate with required cookies and headers
    session: requests.Session = requests.Session()

    # Processes the command-line options
    def __init__(self):
        self.Options = OptionsProcessor.getOptions(sys.argv)

    # Called to update the session tokens required by the service
    @abstractmethod
    def authorize(self, keyId: str= None, keySecret: str= None) -> dict: 
        pass

    # Constructs a fully-qualified URI from the partial service API URI
    @abstractmethod
    def getAbsoluteUri(self, uri: str) -> str:
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
        res = self.__internalCall(get, uri, **kwargs)
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
        res = self.__internalCall(post, uri, **kwargs)
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
        res = self.__internalCall(put, uri, **kwargs)
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
        res = self.__internalCall(delete, uri, **kwargs)
        return res

    # Executes the actual HTTP request using the provided operation function
    def __internalCall(self, httpMethodCall: Callable[[str,dict], requests.Response], uri: str, **kwargs) -> requests.Response:
        uri = self.getAbsoluteUri(uri)

        res = httpMethodCall(uri, **kwargs)
        if res.status_code == 401:
            self.authorize()
            res = httpMethodCall(uri, **kwargs)

        return res

    # Prints the formatted response error to output
    def printResponseError(self, response: requests.Response) -> None:
        """Prints the details of an error response. The code and message (if available).
        Message is formatted by implementing the abstract getErrorMessage method

            Args:

                response: the response returned from the server.
        """
        message = self.getErrorMessage(response)
        code = self.getRespondCodeText(response)
        if message:
            out(f"ASoC Error: {code} - {message}")
        else:
            out(f"ASoC Error: {code}")
    
    @abstractmethod
    def getErrorMessage(self, response: requests.Response) -> str:
        pass

    def getRespondCodeText(self, response: requests.Response) -> HTTPStatus:
        try:
            return HTTPStatus(response.status_code)
        except ValueError:
            return response.status_code

