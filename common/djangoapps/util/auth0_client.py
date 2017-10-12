import requests
import json
import datetime

from django.core.exceptions import ImproperlyConfigured


class Auth0ManagementClient(object):
    __url = None
    __token = {}
    __ttl = 1000 * 60 * 20  # 20 minutes retention

    domainUrl = "https://miro24.eu.auth0.com"
    apiUrl = "https://miro24.eu.auth0.com/api/v2"
    clientId = "PPTNJGiVX37s5PJ9mRg3X43nkwPfcma"
    clientSecret = "3XsT4C88S_PqXr7TZMAULiYBt8M6Uxe_nwZ6uInButlr2CEODeQQ1CcQyZPJJJRy"
    audience = "mirosapi"
    connection = "Username-Password-Authentication"
    connection_id = "con_8kEWS7UQbxq2DqJt"

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
            raise ImproperlyConfigured(
                "Auth0 failed to get token: " + response.text)

        self.__token = response.json()
        self.__token.update({"created_at": datetime.datetime.now()})

    def create_user(self, user):
        self.__refresh_token__()
        url = self.apiUrl + "/users"
        headers = {"Authorization": "Bearer " +
                   self.__token.get("access_token")}
        payload = {"connection": self.connection,
                   "email": user.email, "password": user.password}

        response = requests.post(url, headers=headers, data=payload)
