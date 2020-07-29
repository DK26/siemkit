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

from typing import Tuple

from siemkit.api.arcsight.esm import ArcSightUri
from siemkit.api.arcsight.esm import ArcSightUriEnum


class Login(ArcSightUri):

    def args(self, variables, **kwargs) -> Tuple[str, dict]:
        return (
            '/www/core-service/rest/LoginService/login',
            {
                'headers': {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                'method': 'POST',
                'json': {
                    'log.login': {
                        'log.login': variables.get('username', ''),
                        'log.password': variables.get('password', '')
                    }
                }
            }
        )


class Logout(ArcSightUri):

    def args(self, variables, **kwargs) -> Tuple[str, dict]:
        return (
            '/www/core-service/rest/LoginService/logout',
            {
                'headers': {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                'method': 'POST',
                'json': {
                    "log.logout": {
                        "log.authToken": variables.get('token', '')
                    }
                }
            }
        )


class GetSession(ArcSightUri):

    def args(self, variables, **kwargs) -> Tuple[str, dict]:
        return (
            '/www/core-service/rest/LoginService/getSession',
            {
                'headers': {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Accept': 'application/json'
                },
                'method': 'GET',
                'params': {
                    "authToken": variables.get('token', '')
                }
            }
        )


class LoginApiEnum(ArcSightUriEnum):
    LOGIN = Login()
    LOGOUT = Logout()
    GET_SESSION = GetSession()

