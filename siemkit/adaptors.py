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

from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Union
from typing import Generator
import json


class Keyring(ABC):

    @abstractmethod
    def set_password(self, service: str, key: str, value: str):
        pass

    @abstractmethod
    def get_password(self, service: str, key: str) -> str:
        pass

    @abstractmethod
    def delete_password(self, service: str, key: str):
        pass


class CommonKeyring(Keyring):
    """
    CommonKeyring gets one of the commonly keyring libraries which already implement:
        `set_password()`, `get_password()` & `delete_password()` exactly by these names.

        e.g. `pip install keyring`, `pip install rskeyring` or other.

            import keyring
            adapter = CommonKeyring(keyring)

        could also be:

            import rskeyring
            adapter = CommonKeyring(rskeyring)

        Both can run:

            adatper.set_password(service, key, value)
            adapter.get_password(service, key)
            adapter.delete_password(service, key)

    """

    def __init__(self, module):
        self.__module = module

    def set_password(self, service: str, key: str, value: str):
        self.__module.set_password(service, key, value)

    def get_password(self, service: str, key: str) -> str:
        return self.__module.get_password(service, key)

    def delete_password(self, service: str, key: str):
        self.__module.delete_password(service, key)


class Yaml(ABC):

    @abstractmethod
    def load(self, stream: Any) -> Union[list, dict]:
        pass

    @abstractmethod
    def dump(self, data: Any, stream: Any) -> Any:
        pass


class PyYamlModule(Yaml):

    # pip install PyYAML
    def __init__(self, module):
        if module.__name__ != 'yaml':
            raise Exception("Expected `yaml` module.")

        self.__module = module

    def load(self, stream: Any) -> Union[list, dict]:
        return self.__module.safe_load(stream)

    def dump(self, data: Any, stream: Any) -> Any:
        return self.__module.safe_dump(data, stream, default_flow_style=False)


class Ldap(ABC):

    # Assure usability with `with` context manager
    def __enter__(self):
        pass

    # Assure usability with `with` context manager
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @abstractmethod
    def connect(self,
                server,
                authentication,
                enable_tls,
                tls_validate,
                tls_version,
                user,
                password,
                get_info,
                auto_bind
                ):
        pass

    @abstractmethod
    def get_connection(self):
        pass

    @abstractmethod
    def bind(self):
        pass

    @abstractmethod
    def unbind(self):
        pass

    @abstractmethod
    def search(self, search_base, search_filter, search_scope, attributes):
        pass

    @abstractmethod
    def entries(self) -> Generator[dict, None, None]:
        pass


class Ldap3Module(Ldap):

    # `pip install ldap3`

    def __init__(self, module):

        if module.__name__ != 'ldap3':
            raise Exception("Expected `ldap3` module.")

        self.__module = module

        self.__connection = None

    def connect(self,
                server,
                authentication,
                enable_tls,
                tls_validate,
                tls_version,
                user,
                password,
                get_info,
                auto_bind
                ):

        ldap3_module = self.__module

        tls = None
        if tls_validate and tls_version:
            tls = ldap3_module.Tls(
                validate=tls_validate,
                version=tls_version
            )

        server_info = ldap3_module.Server(
            server,
            get_info=get_info,
            use_ssl=enable_tls,
            tls=tls
        )

        self.__connection = ldap3_module.Connection(
            server_info,
            user=user,
            password=password,
            authentication=authentication,
            auto_bind=auto_bind
        )

        return self.__connection

    def get_connection(self):
        return self.__connection

    def bind(self):
        self.__connection.bind()

    def unbind(self):
        self.__connection.unbind()

    def search(self, search_base, search_filter, search_scope, attributes):
        self.__connection.search(
            search_base=search_base,
            search_filter=search_filter,
            search_scope=search_scope,
            attributes=attributes
        )

    def entries(self) -> Generator[dict, None, None]:
        for entry in self.__connection.entries:
            yield json.loads(entry.entry_to_json())


class HttpResponse(ABC):
    """
    A response container / wrapper to allow safe usage of the HTTP Request adapter.
    """

    @abstractmethod
    def json(self) -> dict:
        pass

    @abstractmethod
    def status_code(self) -> int:
        pass

    @abstractmethod
    def text(self) -> str:
        pass

    @abstractmethod
    def headers(self) -> dict:
        pass

    @abstractmethod
    def cookies(self) -> dict:
        pass


class HttpRequest(ABC):
    """
    Uses the `request` function signature from the `requests` library as basis for the HTTP Request adaptor.
    """

    @abstractmethod
    def request(
            self,
            method,
            url,
            params=None,
            data=None,
            headers=None,
            cookies=None,
            files=None,
            auth=None,
            timeout=None,
            allow_redirects=True,
            proxies=None,
            hooks=None,
            stream=None,
            verify=None,
            cert=None,
            json=None
    ) -> HttpResponse:
        pass


class RequestsModuleResponse(HttpResponse):

    def __init__(self, response):
        self.__response = response

    def status_code(self) -> int:
        return self.__response.status_code

    def text(self) -> str:
        return self.__response.text

    def headers(self) -> dict:
        return self.__response.headers

    def cookies(self) -> dict:
        return self.__response.cookies

    def json(self) -> dict:
        return self.__response.json()


class RequestsModule(HttpRequest):

    def __init__(self, module):
        if module.__name__ != 'requests':
            raise Exception("Expected `requests` module.")

        self.__module = module

    def request(
            self,
            method,
            url,
            params=None,
            data=None,
            headers=None,
            cookies=None,
            files=None,
            auth=None,
            timeout=None,
            allow_redirects=True,
            proxies=None,
            hooks=None,
            stream=None,
            verify=None,
            cert=None,
            json=None
    ) -> HttpResponse:
        requests = self.__module
        response = requests.request(
            method,
            url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=auth,
            timeout=timeout,
            allow_redirects=allow_redirects,
            proxies=proxies,
            hooks=hooks,
            stream=stream,
            verify=verify,
            cert=cert,
            json=json
        )
        return RequestsModuleResponse(response)


class ArcSightEsm(ABC):

    def __init__(
            self,
            http_request_adapter: HttpRequest,
            server: str,
            port: int,
            username: str,
            password: str,
            verify=True,
            cert=None,
            proxies: dict = None
    ):
        pass

    @abstractmethod
    def refresh_token(self, username, password):
        pass

    @abstractmethod
    def request(self, method, uri, headers, payload):
        pass

    @abstractmethod
    def logout(self):
        pass


