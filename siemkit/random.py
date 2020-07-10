#   Copyright (C) 2020 CyberSIEM (R)
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
from .const import TOP_LEVEL_DOMAIN
from .const import DOMAINS
from .const import NAMES


def byte():
    return randint(0, 255)


def compose_ip(amount=1):
    for _ in range(amount):
        yield f"{byte()}.{byte()}.{byte()}.{byte()}"


def compose_domain(amount=1):
    for _ in range(amount):
        yield choice(DOMAINS)


def compose_url(amount=1):

    PROTOCOLS = (
        'http',
        'https'
    )

    for _ in range(amount):
        yield (f"{choice(PROTOCOLS)}://{choice(DOMAINS)}/"
               f"{choice(NAMES).lower()}/{randint(0, 1000)}/"
               f"{choice(NAMES).lower()}?{choice(NAMES).lower()}={randint(0, 1000)}"
               f"&{choice(NAMES).lower()}={randint(0, 1000)}")


def compose_email(amount=1):
    for _ in range(amount):
        yield f"{choice(NAMES).lower()}{randint(10, 80)}@{choice(DOMAINS)}"


def compose_user(amount=1):
    for _ in range(amount):
        yield f"{choice(NAMES)}{choice(NAMES)}{randint(10, 80)}"


def compose_md5(amount=1):
    for _ in range(amount):  # MD5 hex hash size: 32 chars
        yield hex(getrandbits(128))[2:]


def compose_sha1(amount=1):
    for _ in range(amount):  # MD5 hex hash size: 32 chars
        yield hex(getrandbits(160))[2:]


def ip():
    return next(compose_ip())


def md5():
    return next(compose_md5())


def sha1():
    return next(compose_sha1())


def email():
    return next(compose_email())


def url():
    return next(compose_url())


def user():
    return next(compose_user())


def domain():
    return next(compose_domain())

