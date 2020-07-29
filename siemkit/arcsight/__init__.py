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
from enum import EnumMeta

from siemkit.api.arcsight.esm import ArcSightUri
from siemkit.api.arcsight.esm import ArcSightUriEnum
from siemkit.adaptors import RequestsModule
from siemkit.adaptors import HttpResponse

from siemkit.api.arcsight.esm.v72.auth import AuthRequestEnum
from siemkit.api.arcsight.esm.v72.activelist import ActiveListRequestEnum
from siemkit.api.arcsight.esm.v72.events import EventsRequestEnum

import requests

http_request_module = RequestsModule(requests)


class Esm:

    def __init__(
            self,
            server: str,
            port: int,
            username: str,
            password: str,
            verify=True,
            cert=None,
            proxies: dict = None
    ):

        self.__url_base = f"https://{server}:{port}"

        self.__verify = verify
        self.__cert = cert
        self.__proxies = proxies
        self.variables = {
            'token': ''
        }

        self.refresh_token(username, password)

    def refresh_token(self, username, password):

        response = self.uri(
            AuthRequestEnum.LOGIN, {
                'username': username,
                'password': password
            }
        )

        if response.status_code() == 200:

            self.variables['token'] = (
                response.json()
                    .get('log.loginResponse', {})
                    .get('log.return', '')
            )

        return response.status_code()

    def uri(self, api: Union[ArcSightUri, ArcSightUriEnum], variables) -> HttpResponse:

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

    def logout(self):
        response = self.uri(
            AuthRequestEnum.LOGOUT, self.variables
        )
        return response.status_code()

    def get_event_ids(self, event_ids):

        variables = {
            'event_ids': event_ids
        }

        variables.update(self.variables)

        response = self.uri(
            EventsRequestEnum.GET_SECURITY_EVENTS, variables
        )

        if response.status_code() == 200:
            return simplified_cef_events(response)

    def get_activelist_entries(self, resource_id):

        variables = {
            'resource_id': resource_id
        }
        variables.update(self.variables)

        response = self.uri(
            ActiveListRequestEnum.GET_ENTRIES, variables
        )

        return tuple(normalized_active_list_entries(response))


def normalized_active_list_entries(response: HttpResponse):

    if response.status_code() != 200:
        return

    response_json = response.json()
    columns = response_json['act.getEntriesResponse']['act.return']['columns']
    entry_list = response_json['act.getEntriesResponse']['act.return']['entryList']

    for entry in entry_list:
        dict_entry = dict(zip(columns, entry['entry']))
        dict_entry['_columns_order'] = columns
        yield dict_entry


def simple_key_value(complex_cef: dict, prev_key=None):

    for key, value in complex_cef.items():

        if isinstance(prev_key, str):
            # This is a node
            current_key = prev_key + key[0].upper() + key[1:]
        else:
            # This is the root
            current_key = key

        if isinstance(value, dict):
            yield from simple_key_value(value, prev_key=current_key)
        else:
            yield current_key, value


def simplify_cef(complex_cef: dict):

    simple_cef = {}

    for key, item in complex_cef.items():
        if isinstance(item, dict):
            for simple_key, simple_value in simple_key_value(item):
                simple_cef[simple_key] = simple_value
        else:
            simple_cef[key] = item

    return simple_cef


def simplified_cef_events(response: HttpResponse):

    if response.status_code() != 200:
        return

    response_json = response.json()
    complex_cef_events = response_json['sev.getSecurityEventsResponse']['sev.return']

    if isinstance(complex_cef_events, dict):

        # Received a single event
        yield simplify_cef(complex_cef_events)

    else:

        # Received multiple events
        for event in complex_cef_events:
            yield simplify_cef(event)
