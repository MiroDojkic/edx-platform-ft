import requests
import json
import datetime


def with_refresh_token(client_method):

    def wrapper(self, *args):
        if self.is_token_expired():
            self.__refresh_token__()

        return client_method(self, *args)

    return wrapper


class Auth0ManagementClient(object):
    __url = None
    __token = {}
    __ttl = 1000 * 60 * 20  # 20 minutes retention

    domainUrl = ""
    apiUrl = ""
    clientId = ""
    clientSecret = ""
    audience = ""
    connection = ""
    connection_id = ""

    refreshTokenUrl = "https://miro24.eu.auth0.com/oauth/token"

    def __init__(self, url):
        self.__url = url
        self.__refresh_token__()

    def __refresh_token__(self):
        headers = {"content-type": "application/json"}
        payload = {"grant_type": "client_credentials", "client_id": self.clientId,
                   "client_secret": self.clientSecret, "audience": self.audience}

        response = requests.post(self.refreshTokenUrl,
                                 data=json.dumps(payload), headers=headers)

        if response.status_code != 200:
            raise Exception(
                "Auth0 failed to get token: " + response.text)

        self.__token = response.json()
        self.__token.update({"created_at": datetime.datetime.now()})

    def is_token_expired(self):
        return (self.__token.get("created_at") + self.__ttl) < datetime.datetime.now()

    @with_refresh_token
    def create_user(self, email, password):
        url = self.apiUrl + "/users"
        headers = {"Authorization": "Bearer " +
                   self.__token.get("access_token")}
        payload = {"connection": self.connection,
                   "email": email, "password": password}

        response = requests.post(url, headers=headers, data=payload)

        if response.status_code != 201:
            raise Exception(
                "Failed to create user on Auth0: " + response.text)
