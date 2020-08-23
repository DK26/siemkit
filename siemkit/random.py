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
from random import uniform
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
from datetime import datetime
from datetime import timedelta as datetime_timedelta

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


def generate_ip(
        from_address: Union[IPv4Address, str] = '0.0.0.0',
        to_address: Union[IPv4Address, str] = '255.255.255.255',
        amount: int = 1) -> Generator[IPv4Address, None, None]:

    for current_count in range(amount):

        if current_count == amount:
            break

        yield IPv4Address(
            randint(
                int(IPv4Address(from_address)),
                int(IPv4Address(to_address))
            )
        )


def generate_domain(amount: int = 1) -> Generator[str, None, None]:

    for current_count in range(amount):

        if current_count == amount:
            break

        yield choice(DOMAINS)


def generate_url(amount: int = 1) -> Generator[str, None, None]:

    for current_count in range(amount):

        if current_count == amount:
            break

        yield (f"{enum_value(web.Protocol)}://{choice(DOMAINS)}/"
               f"{choice(NAMES).lower()}/{randint(0, 1000)}/"
               f"{choice(NAMES).lower()}?{choice(NAMES).lower()}={randint(0, 1000)}"
               f"&{choice(NAMES).lower()}={randint(0, 1000)}")


def generate_email(amount: int = 1) -> Generator[str, None, None]:

    for current_count in range(amount):

        if current_count == amount:
            break

        yield f"{choice(NAMES).lower()}{randint(10, 80)}@{choice(DOMAINS)}"


def generate_user(amount: int = 1) -> Generator[str, None, None]:

    for current_count in range(amount):

        if current_count == amount:
            break

        yield f"{choice(NAMES)}{choice(NAMES)}{randint(10, 80)}"


def generate_md5(amount: int = 1) -> Generator[str, None, None]:

    for current_count in range(amount):

        if current_count == amount:
            break

        yield hex(getrandbits(128))[2:]


def generate_sha1(amount: int = 1) -> Generator[str, None, None]:

    for current_count in range(amount):

        if current_count == amount:
            break

        yield hex(getrandbits(160))[2:]


def generate_enum_value(*enums: EnumMeta, amount: int = 1) -> Generator[object, None, None]:

    for current_count in range(amount):

        if current_count == amount:
            break

        yield choice(tuple(choice(enums))).value


def generate_http_code(amount: int = 1) -> Generator[int, None, None]:

    for current_count in range(amount):

        if current_count == amount:
            break

        yield enum_value(
            web.HttpInformationalCode,
            web.HttpSuccessCode,
            web.HttpRedirectionCode,
            web.HttpClientErrorCode,
            web.HttpServerErrorCode
        )


def generate_http_information_code(amount: int = 1) -> Generator[int, None, None]:

    for current_count in range(amount):

        if current_count == amount:
            break

        yield enum_value(web.HttpInformationalCode)


def generate_http_success_code(amount: int = 1) -> Generator[int, None, None]:

    for current_count in range(amount):

        if current_count == amount:
            break

        yield enum_value(web.HttpSuccessCode)


def generate_http_redirection_code(amount: int = 1) -> Generator[int, None, None]:

    for current_count in range(amount):

        if current_count == amount:
            break

        yield enum_value(web.HttpRedirectionCode)


def generate_http_error_code(amount: int = 1) -> Generator[int, None, None]:

    for current_count in range(amount):

        if current_count == amount:
            break

        yield enum_value(
            web.HttpClientErrorCode,
            web.HttpServerErrorCode
        )


def generate_http_client_error_code(amount: int = 1) -> Generator[int, None, None]:

    for current_count in range(amount):

        if current_count == amount:
            break

        yield enum_value(web.HttpClientErrorCode)


def generate_http_server_error_code(amount: int = 1) -> Generator[int, None, None]:

    for current_count in range(amount):

        if current_count == amount:
            break

        yield enum_value(web.HttpServerErrorCode)


def generate_flag_value(*enums: EnumMeta, amount: int = 1, flags: int = 1) -> Generator[int, None, None]:

    for current_count in range(amount):

        if current_count == amount:
            break

        random_flag = 0

        for _ in range(flags):
            random_flag = flag.set_on(random_flag, choice(tuple(choice(enums))))

        yield random_flag


def generate_port(from_port: int = 0, to_port: int = 65535, amount: int = 1) -> Generator[int, None, None]:

    if not (0 <= from_port <= to_port <= 65535):
        raise ValueError("Illegal port range. Legal port range 0-65535.")

    for current_count in range(amount):

        if current_count == amount:
            break

        yield randint(from_port, to_port)


def generate_timedelta(
        start_timedelta: datetime_timedelta,
        end_timedelta: datetime_timedelta,
        amount: int = 1
) -> Generator[datetime_timedelta, None, None]:

    for current_count in range(amount):

        if current_count == amount:
            break

        yield datetime_timedelta(
            seconds=uniform(
                start_timedelta.total_seconds(),
                end_timedelta.total_seconds()
            )
        )


def generate_time(
        start_time: datetime = None,
        end_time: datetime = None,
        gap: datetime_timedelta = None,
        amount: int = 1
) -> Generator[datetime, None, None]:

    if end_time is None and isinstance(start_time, datetime) and isinstance(gap, datetime_timedelta):
        # Gap forward in time
        end_time = start_time + gap

    elif start_time is None and isinstance(end_time, datetime) and isinstance(gap, datetime_timedelta):
        # Gap back in time
        start_time = end_time - gap

    elif start_time is None and end_time is None:

        # Default

        end_time = datetime.now()

        if gap is None:
            start_time = end_time - datetime_timedelta(minutes=1)
        else:
            start_time = end_time - gap

    for current_count in range(amount):

        if current_count == amount:
            break

        yield datetime.fromtimestamp(
            uniform(
                start_time.timestamp(), end_time.timestamp()
            )
        )


def enum_value(*enums: EnumMeta) -> object:
    return next(generate_enum_value(*enums, amount=1))


def flag_value(*enums: EnumMeta, flags=1) -> int:
    return next(generate_flag_value(*enums, flags=flags))


def ip(from_address: Union[IPv4Address, str] = '0.0.0.0',
       to_address: Union[IPv4Address, str] = '255.255.255.255') -> IPv4Address:

    return next(
        generate_ip(
            from_address=from_address,
            to_address=to_address
        )
    )


def port(from_port: int = 0, to_port: int = 65535) -> int:

    return next(
        generate_port(
            from_port=from_port,
            to_port=to_port
        )
    )


def md5() -> str:
    return next(generate_md5())


def sha1() -> str:
    return next(generate_sha1())


def email() -> str:
    return next(generate_email())


def url() -> str:
    return next(generate_url())


def user() -> str:
    return next(generate_user())


def domain() -> str:
    return next(generate_domain())


def http_code() -> int:
    return next(generate_http_code())


def http_information_code() -> int:
    return next(generate_http_information_code())


def http_success_code() -> int:
    return next(generate_http_success_code())


def http_error_code() -> int:
    return next(generate_http_error_code())


def http_client_error_code() -> int:
    return next(generate_http_client_error_code())


def http_redirection_code() -> int:
    return next(generate_http_redirection_code())


def http_server_error_code() -> int:
    return next(generate_http_server_error_code())


def time(start_time: datetime = None, end_time: datetime = None, gap: datetime_timedelta = None) -> datetime:
    return next(generate_time(start_time, end_time, gap))


def timedelta(start_timedelta: datetime_timedelta, end_timedelta: datetime_timedelta) -> datetime_timedelta:
    return next(generate_timedelta(start_timedelta, end_timedelta))
