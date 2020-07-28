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

from siemkit.api.arcsight.esm import ArcSightUri
from siemkit.adaptors import RequestsModule
from siemkit.adaptors import HttpResponse

from siemkit.api.arcsight.esm.v72 import auth
from siemkit.api.arcsight.esm.v72 import activelist
from siemkit.api.arcsight.esm.v72 import events

import requests

http_request_module = RequestsModule(requests)


class Esm:

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

        self.__verify = verify
        self.__cert = cert
        self.__proxies = proxies
        self.variables = {
            'token': ''
        }

        self.refresh_token(username, password)

    def refresh_token(self, username, password):

        response = self.uri(
            auth.Login(), {
                'username': username,
                'password': password
            }
        )

        if response.status_code() == 200:

            self.variables['token'] = (
                response.json()
                    .get('log.loginResponse', {})
                    .get('log.return', '')
            )

        return response.status_code()

    def uri(self, api: ArcSightUri, variables) -> HttpResponse:

        uri, request_args = api.args(variables=variables)

        request_args.update(
            {
                'url': f"{self.__base_uri}{uri}"
            }
        )

        return http_request_module.request(**request_args)

    def logout(self):
        response = self.uri(
            auth.Logout(), self.variables
        )
        return response.status_code()

    def get_event_ids(self, event_ids):
        pass

    def get_activelist(self, resource_id):
        pass

