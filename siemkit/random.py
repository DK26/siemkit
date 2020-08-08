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

from random import randint
from random import getrandbits
from random import choice

from ipaddress import IPv4Address
from typing import Generator
from typing import Union
from enum import EnumMeta

import os
import threading
from time import time
from math import floor

from .const import DOMAINS
from .const import NAMES
from . import web
from . import flag


def safe_object_uuid(obj: object) -> str:
    object_id = hex(id(obj))[2:]
    process_id = hex(os.getpid())[2:]
    timestamp = hex(floor(time() * 1e5))[2:]
    thread_id = hex(threading.get_ident())[2:]
    random_value = hex(getrandbits(32))[2:]

    return f'{object_id}-{process_id}-{thread_id}-{timestamp}-{random_value}'


def byte() -> int:
    return randint(0, 255)


def compose_ip(
        from_address: Union[IPv4Address, str] = '0.0.0.0',
        to_address: Union[IPv4Address, str] = '255.255.255.255',
        amount: int = 1) -> Generator[IPv4Address, None, None]:

    for _ in range(amount):

        yield IPv4Address(
            randint(
                int(IPv4Address(from_address)),
                int(IPv4Address(to_address))
            )
        )


def compose_domain(amount: int = 1) -> Generator[str, None, None]:
    for _ in range(amount):
        yield choice(DOMAINS)


def compose_url(amount: int = 1) -> Generator[str, None, None]:

    for _ in range(amount):
        yield (f"{enum_value(web.Protocol)}://{choice(DOMAINS)}/"
               f"{choice(NAMES).lower()}/{randint(0, 1000)}/"
               f"{choice(NAMES).lower()}?{choice(NAMES).lower()}={randint(0, 1000)}"
               f"&{choice(NAMES).lower()}={randint(0, 1000)}")


def compose_email(amount: int = 1) -> Generator[str, None, None]:
    for _ in range(amount):
        yield f"{choice(NAMES).lower()}{randint(10, 80)}@{choice(DOMAINS)}"


def compose_user(amount: int = 1) -> Generator[str, None, None]:
    for _ in range(amount):
        yield f"{choice(NAMES)}{choice(NAMES)}{randint(10, 80)}"


def compose_md5(amount: int = 1) -> Generator[str, None, None]:
    for _ in range(amount):
        yield hex(getrandbits(128))[2:]


def compose_sha1(amount: int = 1) -> Generator[str, None, None]:
    for _ in range(amount):
        yield hex(getrandbits(160))[2:]


def compose_enum_value(*enums: EnumMeta, amount: int = 1) -> Generator[object, None, None]:
    for _ in range(amount):
        yield choice(tuple(choice(enums))).value


def compose_http_code(amount: int = 1) -> Generator[int, None, None]:
    for _ in range(amount):
        yield enum_value(
            web.HttpInformationalCode,
            web.HttpSuccessCode,
            web.HttpRedirectionCode,
            web.HttpClientErrorCode,
            web.HttpServerErrorCode
        )


def compose_http_information_code(amount: int = 1) -> Generator[int, None, None]:
    for _ in range(amount):
        yield enum_value(web.HttpInformationalCode)


def compose_http_success_code(amount: int = 1) -> Generator[int, None, None]:
    for _ in range(amount):
        yield enum_value(web.HttpSuccessCode)


def compose_http_redirection_code(amount: int = 1) -> Generator[int, None, None]:
    for _ in range(amount):
        yield enum_value(web.HttpRedirectionCode)


def compose_http_error_code(amount: int = 1) -> Generator[int, None, None]:
    for _ in range(amount):
        yield enum_value(
            web.HttpClientErrorCode,
            web.HttpServerErrorCode
        )


def compose_http_client_error_code(amount: int = 1) -> Generator[int, None, None]:
    for _ in range(amount):
        yield enum_value(web.HttpClientErrorCode)


def compose_http_server_error_code(amount: int = 1) -> Generator[int, None, None]:
    for _ in range(amount):
        yield enum_value(web.HttpServerErrorCode)


def compose_flag_value(*enums: EnumMeta, amount: int = 1, flags: int = 1) -> Generator[int, None, None]:
    for _ in range(amount):

        random_flag = 0

        for _ in range(flags):
            random_flag = flag.set_on(random_flag, choice(tuple(choice(enums))))

        yield random_flag


def enum_value(*enums: EnumMeta) -> object:
    return next(compose_enum_value(*enums, amount=1))


def flag_value(*enums: EnumMeta, flags=1) -> int:
    return next(compose_flag_value(*enums, flags=flags))


def ip(from_address: Union[IPv4Address, str] = '0.0.0.0',
       to_address: Union[IPv4Address, str] = '255.255.255.255') -> IPv4Address:

    return next(
        compose_ip(
            from_address=from_address,
            to_address=to_address
        )
    )


def md5() -> str:
    return next(compose_md5())


def sha1() -> str:
    return next(compose_sha1())


def email() -> str:
    return next(compose_email())


def url() -> str:
    return next(compose_url())


def user() -> str:
    return next(compose_user())


def domain() -> str:
    return next(compose_domain())


def http_code() -> int:
    return next(compose_http_code())


def http_information_code() -> int:
    return next(compose_http_information_code())


def http_success_code() -> int:
    return next(compose_http_success_code())


def http_error_code() -> int:
    return next(compose_http_error_code())


def http_client_error_code() -> int:
    return next(compose_http_client_error_code())


def http_redirection_code() -> int:
    return next(compose_http_redirection_code())


def http_server_error_code() -> int:
    return next(compose_http_server_error_code())

