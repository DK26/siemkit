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

from typing import Union
from collections.abc import Iterable

import urllib3
import requests
import zlib

from siemkit.api.arcsight.esm import ArcSightUri
from siemkit.api.arcsight.esm import ArcSightUriEnum
from siemkit.adaptors import RequestsModule
from siemkit.adaptors import HttpResponse

from siemkit.data import RamKeyring
from siemkit.data import Vault

from siemkit.api.arcsight.esm.v72.auth import LoginApiEnum
from siemkit.api.arcsight.esm.v72.activelist import ActiveListApiEnum
from siemkit.api.arcsight.esm.v72.events import EventsApiEnum

http_request_module = RequestsModule(requests)
urllib3.disable_warnings()


class Esm:

    def __init__(
            self,
            server: str,
            port: int,
            username: str,
            password: str,
            verify=True,
            cert=None,
            proxies: dict = None,
            vault: Vault = None
    ):

        server_id = f"{server}:{port}"
        self.__url_base = f"https://{server_id}"

        self.__verify = verify
        self.__cert = cert
        self.__proxies = proxies

        self.variables = {
            'token': ''
        }

        self.__server_id = hex(
            zlib.crc32(
                bytes(server_id, 'utf-8')
            )
        )[2:]

        self.__vault_name = f'arcsight.esm.{self.__server_id}'

        if vault is None:
            # For now, we are using an unsafe RAM Keyring until we can figure out
            # something better as default.
            vault = Vault(self.__vault_name, keyring_adaptor=RamKeyring())

        self.__vault = vault

        # vault.store_secret('username', username)
        # vault.store_secret('password', password)

        # self._activelist_columns = {}

        self.refresh_token(username, password)

    def refresh_token(self, username=None, password=None):

        if isinstance(username, str):
            self.__vault.store_secret('username', username)

        if isinstance(password, str):
            self.__vault.store_secret('password', password)

        response = self.unchecked_uri(
            LoginApiEnum.LOGIN, {
                'username': self.__vault.get_secret('username'),
                'password': self.__vault.get_secret('password')
            }
        )

        if response.status_code() == 200:

            self.variables['token'] = (
                response.json()
                    .get('log.loginResponse', {})
                    .get('log.return', '')
            )

        return response.status_code()

    def maintain_session(self):
        response = self.get_session()
        if response.status_code() == 500:
            self.refresh_token()

    def unchecked_uri(self, api: Union[ArcSightUri, ArcSightUriEnum], variables) -> HttpResponse:

        if isinstance(api, ArcSightUriEnum):
            api = api.value

        uri, request_args = api.args(variables=variables)

        request_args.update(
            {
                'url': f"{self.__url_base}{uri}",
                'verify': self.__verify,
                'cert': self.__cert,
                'proxies': self.__proxies
            }
        )

        return http_request_module.request(**request_args)

    def uri(self, api: Union[ArcSightUri, ArcSightUriEnum], variables) -> HttpResponse:

        # self.maintain_session()  # Exposed token in URL

        return self.unchecked_uri(api=api, variables=variables)

    def logout(self):

        response = self.unchecked_uri(
            LoginApiEnum.LOGOUT, self.variables
        )

        self.__vault.delete_secret('username')
        self.__vault.delete_secret('password')

        return response.status_code()

    def get_session(self):

        response = self.unchecked_uri(
            LoginApiEnum.GET_SESSION, self.variables
        )

        return response

    def get_event_ids(self, *event_ids):

        def extract_ids():
            for event_id in event_ids:
                if isinstance(event_id, int):
                    yield event_id
                elif isinstance(event_id, str):
                    yield int(event_id)
                elif isinstance(event_id, Iterable):
                    for id_ in event_id:
                        yield int(id_)

        variables = {
            'event_ids': list(extract_ids())
        }

        variables.update(self.variables)

        response = self.uri(
            EventsApiEnum.GET_SECURITY_EVENTS, variables
        )

        response_json = response.json()

        sev_get_security_events_response = response_json.get('sev.getSecurityEventsResponse')

        has_entries = 'sev.return' in sev_get_security_events_response

        if response.status_code() != 200:
            raise Exception(f"(Response {response.status_code()}) "
                            f"Could not retrieve event IDs '{' ,'.join(event_ids)}'.")
        elif not has_entries:
            raise Exception(f"Event IDs '{' ,'.join((str(event_id) for event_id in event_ids))}' were not found.")

        return simplified_cef_events(response)

    def get_activelist(self, resource_id):

        variables = {
            'resource_id': resource_id
        }
        variables.update(self.variables)  # Get the token

        response = self.uri(
            ActiveListApiEnum.GET_ENTRIES, variables
        )

        if response.status_code() != 200:
            raise Exception(f"(Response {response.status_code()}) "
                            f"Could not retrieve resource ID '{resource_id}'.")

        entries = tuple(normalized_active_list_entries(response))

        # if entries:
        #     self._activelist_columns[resource_id] = entries[0].get('_columns_order')

        return entries

    def delete_activelist_entries(self, resource_id, entries):

        # columns = self._activelist_columns.get(resource_id)
        # if columns is None:
        #     self.get_activelist(resource_id)  # Update columns just by querying.
        #     columns = self._activelist_columns.get(resource_id)

        if not entries:
            return

        if isinstance(entries, dict):
            columns = entries['_columns_order']
        elif not isinstance(entries, str) and hasattr(entries, '__getitem__'):
            columns = entries[0]['_columns_order']
        else:
            raise TypeError(f"Illegal entries object: {entries}")

        variables = {
            'resource_id': resource_id,
            'columns': columns,
            'entries': entries
        }
        variables.update(self.variables)  # Get the token

        response = self.uri(
            ActiveListApiEnum.DELETE_ENTRIES, variables
        )

        if response.status_code() != 204:
            raise Exception(f"(Response {response.status_code()}) "
                            f"Could not delete entries of resource ID '{resource_id}'.")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_tb:
                raise
        finally:
            self.logout()


def normalized_active_list_entries(response: HttpResponse):

    if response.status_code() != 200:
        return

    response_json = response.json()
    columns = response_json['act.getEntriesResponse']['act.return']['columns']
    entry_list = response_json['act.getEntriesResponse']['act.return'].get('entryList')

    if entry_list is None:
        return

    # Single Result
    if isinstance(entry_list, dict):
        dict_entry = dict(zip(columns, entry_list['entry']))
        dict_entry['_columns_order'] = columns
        yield dict_entry

    # Multiple Results
    elif isinstance(entry_list, list):
        for entry in entry_list:
            dict_entry = dict(zip(columns, entry['entry']))
            dict_entry['_columns_order'] = columns
            yield dict_entry


def simple_key_value(complex_cef: dict, prev_key):

    for key, value in complex_cef.items():

        current_key = prev_key + key[0].upper() + key[1:]

        if isinstance(value, dict):
            yield from simple_key_value(value, prev_key=current_key)
        else:
            yield current_key, value


def simplify_cef(complex_cef: dict):

    simple_cef = {}

    for key, item in complex_cef.items():
        if isinstance(item, dict):
            for simple_key, simple_value in simple_key_value(item, key):
                simple_cef[simple_key] = simple_value
        else:
            simple_cef[key] = item

    return simple_cef


def simplified_cef_events(response: HttpResponse):

    if response.status_code() != 200:
        return

    response_json = response.json()

    sev_get_security_events_response = response_json.get('sev.getSecurityEventsResponse')

    if 'sev.return' not in sev_get_security_events_response:
        return

    complex_cef_events = sev_get_security_events_response.get('sev.return')

    if isinstance(complex_cef_events, dict):

        # Received a single event
        yield simplify_cef(complex_cef_events)

    else:

        # Received multiple events
        for event in complex_cef_events:
            yield simplify_cef(event)
