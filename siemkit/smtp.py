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

import smtplib
import ssl
from typing import Generator
from typing import Collection
from abc import abstractmethod
import zlib
import re
import os

from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

from siemkit.data import Vault
from siemkit.data import RamKeyring


class SmtpLogin:

    def __init__(self, server, port, username=None, password=None, vault: Vault = None):

        self.__server = server
        self.__port = port

        server_id = f"{server}:{port}"

        self.__server_id = hex(
            zlib.crc32(
                bytes(server_id, 'utf-8')
            )
        )[2:]

        self.__vault_name = f'smtp.{self.__server_id}'

        if vault is None:
            # For now, we are using an unsafe RAM Keyring until we can figure out
            # something better as default.
            vault = Vault(self.__vault_name, keyring_adaptor=RamKeyring())

        self.__vault = vault

        self.__vault.store_secret('username', username)
        self.__vault.store_secret('password', password)

    @abstractmethod
    def login(self) -> smtplib.SMTP:
        pass


class GmailTlsLogin(SmtpLogin):
    """
    Current Requirements: an `App Password` must be created for this to work.
        However GMail change their security protocols on regular basis. Any changes should be
        documented & updated here.
    """

    def __init__(self, server, port, username=None, password=None, vault: Vault = None):
        super().__init__(server, port, username, password, vault)
        self.__context = ssl.create_default_context()
        self.__smtp_session = None

    def login(self) -> smtplib.SMTP:

        self.__smtp_session = smtplib.SMTP(self.__server, self.__port)
        self.__smtp_session.ehlo()
        self.__smtp_session.starttls(context=self.__context)

        self.__smtp_session.login(
            self.__vault.get_secret('username'),
            self.__vault.get_secret('password')
        )

        return self.__smtp_session


class BasicLogin(SmtpLogin):

    def __init__(self, server, port, username=None, password=None, vault: Vault = None):
        super().__init__(server, port, username, password, vault)
        self.__smtp_session = None

    def login(self, username=None, password=None, vault: Vault = None):
        self.__smtp_session = smtplib.SMTP(self.__server, self.__port)
        return self.__smtp_session


class Connection:

    def __init__(self, smtp_login: SmtpLogin):
        self.__smtp_session = smtp_login.login()

    def sendmail(self, from_address, to_addresses, cc_addresses, bcc_addresses, smtp_mime_payload):
        self.__smtp_session.sendmail(
            from_address,
            to_addresses + cc_addresses + bcc_addresses,
            smtp_mime_payload.as_string()
        )

    def get_session(self) -> smtplib.SMTP:
        return self.__smtp_session

    def quit(self):
        return self.__smtp_session.quit()


def map_images(html_content: str) -> dict:

    images = re.findall(r'src=["]?(.*?)["]?[\s\>]', html_content, flags=re.MULTILINE)
    images_paths = set()
    images_map = {}

    for image_id, image_path in enumerate(images):
        if image_path not in images_paths:
            images_map[f'image_{image_id}'] = image_path
            images_paths.add(image_path)

    return images_map


def create_mime_images(work_dir: str, images_map: dict) -> Generator[MIMEImage, None, None]:

    for image_id, image_path in images_map.items():

        with open(os.path.join(work_dir, image_path), 'rb') as fs:
            mime_image = MIMEImage(fs.read())

        mime_image.add_header('Content-ID', f'<{image_id}>')

        yield mime_image


def attach_images(smtp_mime_multipart: MIMEMultipart, mime_images: Collection) -> MIMEMultipart:

    for mime_image in mime_images:
        smtp_mime_multipart.attach(mime_image)

    return smtp_mime_multipart


def embed_images(html_content: str, images_map: dict) -> str:

    for image_id, image_path in images_map.items():
        html_content = html_content.replace(image_path, f'cid:{image_id}')

    return html_content


