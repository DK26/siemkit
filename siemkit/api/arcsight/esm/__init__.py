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
from abc import abstractmethod
from typing import Tuple


class ArcSightUri(ABC):

    @abstractmethod
    def args(self, variables) -> Tuple[str, dict]:
        pass


class ArcSightLoginOld(ArcSightUri):

    def __init__(self, variables):
        super().__init__(variables)
        self.variables = variables

        server = variables.args('server', '127.0.0.1')
        port = variables.args('port', 8443)
        verify = variables.args('verify', True)
        cert = variables.args('cert')
        proxies = variables.args('proxies')

        self.__request = {
            'headers': {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            'method': 'POST',
            'url': f'https://{server}:{port}/www/core-service/rest/LoginService/login',
            'json': {
                'log.login': {
                    'log.login': variables.args('username', ''),
                    'log.password': variables.args('password', '')
                }
            },
            'verify': verify,
            'cert': cert,
            'proxies': proxies
        }

    def args(self) -> dict:
        return self.__request


