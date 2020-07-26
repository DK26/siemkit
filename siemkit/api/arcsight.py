#   Copyright (C) 2020 CyberSIEM(R)
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from enum import Enum
from abc import ABC


class ArcSightUri:

    def __init__(self, method, uri, headers, payload):
        self.method = method
        self.uri = uri
        self.headers = headers
        self.payload = payload


class ArcSightLogin(ArcSightUri):
    pass


arcsight_login = {
    'headers': {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    },
    'method': 'POST',
    'uri': '/www/core-service/rest/LoginService/login',
    'payload': {
            'log.login': {
                'log.login': '{{username}}',
                'log.password': '{{password}}'
            }
    }
}


class Uri(str, Enum):
    pass


class ArcSightEsm:

    def __init__(
            self,
            server: str,
            port: int,
            username: str,
            password: str,
            verify=True,
            cert=None,
            proxies: dict = None
    ):

        self.__base_uri = f"https://{server}:{port}"
        self.verify = verify
        self.cert = cert
        self.proxies = proxies

        self.__api_token = ''
        self.refresh_token(username, password)

    def refresh_token(self, username, password):

        uri = f'{self.__base_uri}/www/core-service/rest/LoginService/login'

    def query(self, query):
        pass

    def logout(self):
        pass

