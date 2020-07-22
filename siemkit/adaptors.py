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

