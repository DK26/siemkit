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
from typing import Callable
from typing import Iterable
from typing import Type
from abc import abstractmethod
from abc import ABC
from enum import Enum

import zlib
import re
import os

from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from siemkit.data import Vault
from siemkit.data import RamKeyring

from siemkit import html


class AuthenticationEnum(str, Enum):
    NO_AUTH = 'noauth'
    STARTTLS = 'starttls'
    TLS = 'tls'

    def __str__(self):
        return self.value


class SmtpAuthentication:
    module_name = 'undefined'

    def __init__(self, server, port, username=None, password=None, vault: Vault = None):
        self._server = server
        self._port = port

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

        self._vault = vault

        self._vault.store_secret('username', username)
        self._vault.store_secret('password', password)

    @abstractmethod
    def connect(self) -> smtplib.SMTP:
        pass


class TlsAuth(SmtpAuthentication):
    """
    Start a secure SSL/TLS connection before authenticating.
    A failure will abort the connection.
    """

    module_name = 'tls'

    def __init__(self, server, port=465, username=None, password=None, vault: Vault = None):
        super().__init__(server, port, username, password, vault)
        self.__smtp_session = None

    def connect(self) -> smtplib.SMTP:
        self.__smtp_session = smtplib.SMTP_SSL(self._server, self._port)

        self.__smtp_session.login(
            self._vault.get_secret('username'),
            self._vault.get_secret('password')
        )

        return self.__smtp_session


class StarttlsAuth(SmtpAuthentication):
    """
    Attempt to establish a secure SSL/TLS connection before authenticating.
    A failure may allow an insecure connection.
    """

    module_name = 'starttls'

    def __init__(self, server, port=587, username=None, password=None, vault: Vault = None):
        super().__init__(server, port, username, password, vault)
        self.__context = ssl.create_default_context()
        self.__smtp_session = None

    def connect(self) -> smtplib.SMTP:
        self.__smtp_session = smtplib.SMTP(self._server, self._port)
        self.__smtp_session.ehlo()
        self.__smtp_session.starttls(context=self.__context)

        self.__smtp_session.login(
            self._vault.get_secret('username'),
            self._vault.get_secret('password')
        )

        return self.__smtp_session


class NoAuth(SmtpAuthentication):
    """
    SMTP default insecure open mail relay connection with no authentication.
    """

    module_name = 'noauth'

    def __init__(self, server, port=25, username=None, password=None, vault: Vault = None):
        super().__init__(server, port, username, password, vault)
        self.__smtp_session = None

    def connect(self, username=None, password=None, vault: Vault = None):
        self.__smtp_session = smtplib.SMTP(self._server, self._port)
        return self.__smtp_session

    def get_session(self) -> smtplib.SMTP:
        return self.__smtp_session

    def quit(self):
        return self.__smtp_session.quit()


def map_images(html_content: str) -> dict:
    images = re.findall(r'^.*?<.*?src=["]?([^;>=]+?)["]?(?:>|\s\w+=)', html_content, flags=re.MULTILINE)
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


def attach_images(smtp_mime_multipart: MIMEMultipart, mime_images: Iterable) -> MIMEMultipart:
    for mime_image in mime_images:
        smtp_mime_multipart.attach(mime_image)

    return smtp_mime_multipart


def embed_images(html_content: str, images_map: dict) -> str:
    for image_id, image_path in images_map.items():
        html_content = html_content.replace(image_path, f'cid:{image_id}')

    return html_content


def attach_files(smtp_mime_multipart: MIMEMultipart, files: Iterable) -> MIMEMultipart:

    if isinstance(files, str):
        files = [files]

    for file in files:

        if not os.path.exists(file):
            continue

        file_name = os.path.basename(file)
        with open(file, "rb") as fs:
            attachment = MIMEApplication(
                fs.read(),
                Name=file_name
            )

        attachment['Content-Disposition'] = f'attachment; filename="{file_name}"'
        smtp_mime_multipart.attach(attachment)

    return smtp_mime_multipart


class MimeMessage(ABC):

    def __init__(
            self,
            from_address,
            to_addresses,
            cc_addresses=None,
            bcc_addresses=None,
    ):

        self._from_address = None
        self._to_addresses = None
        self._cc_addresses = None
        self._bcc_addresses = None

        self.from_address = from_address
        self.to_addresses = to_addresses
        self.cc_addresses = cc_addresses
        self.bcc_addresses = bcc_addresses

    @classmethod
    def init_addresses(cls, addresses):

        if addresses is None:
            return []
        elif isinstance(addresses, str):
            return [addresses]
        elif isinstance(addresses, Iterable):
            return list(addresses)

    @abstractmethod
    def as_string(self) -> str:
        pass

    @property
    def from_address(self):
        return self._from_address

    @from_address.setter
    def from_address(self, value):
        self._from_address = value

    @property
    def to_addresses(self):
        return self._to_addresses

    @to_addresses.setter
    def to_addresses(self, value):
        self._to_addresses = MimeMessage.init_addresses(value)

    @property
    def cc_addresses(self):
        return self._cc_addresses

    @cc_addresses.setter
    def cc_addresses(self, value):
        self._cc_addresses = MimeMessage.init_addresses(value)

    @property
    def bcc_addresses(self):
        return self._bcc_addresses

    @bcc_addresses.setter
    def bcc_addresses(self, value):
        self._bcc_addresses = MimeMessage.init_addresses(value)


class MultipartMimeMessage(MimeMessage):

    def __init__(
            self,
            from_address,
            to_addresses,
            cc_addresses=None,
            bcc_addresses=None,
            subject='',
            content='',
            content_render: Callable = None,
            content_variables: dict = None,
            work_dir=None,
            attachments=None,
            encoding='utf-8'
    ):

        super().__init__(from_address, to_addresses, cc_addresses, bcc_addresses)

        # Prep Base
        self.__smtp_multipart = MIMEMultipart()
        self.__smtp_multipart['From'] = from_address
        self.__smtp_multipart['To'] = ','.join(self.to_addresses)
        self.__smtp_multipart['CC'] = ','.join(self.cc_addresses)
        self.__smtp_multipart['Subject'] = subject
        self.subject = subject

        if work_dir is None:
            work_dir = ''
        self._work_dir = work_dir

        # Prep Content
        if os.path.exists(content):
            self._work_dir = os.path.dirname(content)

            with open(content, 'r', encoding=encoding, errors='ignore') as fs:
                content = fs.read()

        if callable(content_render):
            content = content_render(content, content_variables)

        content = html.remove_comments(content)

        images_map = map_images(content)

        if images_map:
            content = embed_images(content, images_map)

            # Load Images
            image_loader = create_mime_images(self._work_dir, images_map)
            attach_images(self.__smtp_multipart, image_loader)

        self.__smtp_multipart.attach(
            MIMEText(content, 'html', _charset=encoding)
        )

        self.content = content

        # Load Attachments
        if attachments is not None:

            if isinstance(attachments, str):
                attachments = [attachments]

            attach_files(self.__smtp_multipart, attachments)

    def __str__(self):
        return str(self.__smtp_multipart)

    def as_string(self):
        return self.__smtp_multipart.as_string()

    def get_smtp_multipart(self):
        return self.__smtp_multipart


class Connection:

    def __init__(self, smtp_login: SmtpAuthentication):
        self.__smtp_session = smtp_login.connect()

    # def sendmail(self, from_address, send_addresses, smtp_mime_payload):
    #
    #     send_to = []
    #     if isinstance(send_addresses, str):
    #         send_to.append(send_addresses)
    #     elif isinstance(send_addresses, Iterable):
    #         for address in send_addresses:
    #             if isinstance(address, str):
    #                 send_to.append(address)
    #             else:
    #                 send_to.extend(address)
    #
    #     self.__smtp_session.sendmail(
    #         from_address,
    #         send_to,
    #         smtp_mime_payload.as_string()
    #     )

    def sendmail(self, smtp_mime_payload: MimeMessage):

        from_address = smtp_mime_payload.from_address
        to_addresses = smtp_mime_payload.to_addresses
        cc_addresses = smtp_mime_payload.cc_addresses
        bcc_addresses = smtp_mime_payload.bcc_addresses

        send_to = []

        for addresses_batch in (to_addresses, cc_addresses, bcc_addresses):

            if isinstance(addresses_batch, str):
                send_to.append(addresses_batch)
            elif isinstance(addresses_batch, Iterable):
                for address in addresses_batch:
                    if isinstance(address, str):
                        send_to.append(address)
                    else:
                        send_to.extend(address)

        self.__smtp_session.sendmail(
            from_address,
            send_to,
            smtp_mime_payload.as_string()
        )


class AuthenticationModuleFactory:

    def __init__(self):
        self._modules = {}

    def register_module(self, module: Type[SmtpAuthentication]):
        self._modules[module.module_name] = module
        return self

    def create(self, module_name, **kwargs):
        module = self._modules.get(module_name)
        if module is None:
            raise ValueError(module_name)

        return self._modules[module_name](**kwargs)


AUTH_MODULE_FACTORY = AuthenticationModuleFactory()

AUTH_MODULE_FACTORY.register_module(TlsAuth)
AUTH_MODULE_FACTORY.register_module(StarttlsAuth)
AUTH_MODULE_FACTORY.register_module(NoAuth)


