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
            pass

    def get_activelist_entries(self, resource_id):

        variables = {
            'resource_id': resource_id
        }
        variables.update(self.variables)

        response = self.uri(
            ActiveListRequestEnum.GET_ENTRIES, variables
        )


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


"""
{
    "sev.getSecurityEventsResponse": {
        "sev.return": {
            "agent": {
                "mutable": true,
                "address": 174351991,
                "addressAsBytes": "CmRmdw==",
                "assetId": "4paH4P3EBABCSMnSiDweTZg==",
                "assetLocalId": 17179869193,
                "assetName": "linuxconn",
                "hostName": "linuxconn",
                "macAddress": 52229671306,
                "translatedAddress": -9223372036854775808,
                "zone": {
                    "id": "ML8022AABABCDTFpYAT3UdQ==",
                    "isModifiable": false,
                    "managerID": "UUQVDXEBABCAXSH6KyOOWw==",
                    "referenceID": 2084,
                    "referenceName": "Zone",
                    "referenceString": "<Resource URI=\"/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 10.0.0.0-10.255.255.255\" ID=\"ML8022AABABCDTFpYAT3UdQ==\"/>",
                    "referenceType": 29,
                    "uri": "/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 10.0.0.0-10.255.255.255"
                },
                "timeZone": "Asia/Jerusalem",
                "version": "7.15.0.8295.0",
                "id": "3CgN77nEBABDaCRMDAaJaBw==",
                "name": "syslog_10525",
                "type": "syslog"
            },
            "agentReceiptTime": 1595968655010,
            "agentSeverity": 0,
            "aggregatedEventCount": 1,
            "assetCriticality": 0,
            "baseEventCount": 1,
            "bytesIn": -2147483648,
            "bytesOut": -2147483648,
            "concentratorAgents": {
                "mutable": true,
                "address": 174351991,
                "addressAsBytes": "CmRmdw==",
                "assetId": "4paH4P3EBABCSMnSiDweTZg==",
                "assetLocalId": 17179869193,
                "assetName": "linuxconn",
                "hostName": "linuxconn",
                "macAddress": 52229671306,
                "translatedAddress": -9223372036854775808,
                "zone": {
                    "id": "ML8022AABABCDTFpYAT3UdQ==",
                    "isModifiable": false,
                    "managerID": "UUQVDXEBABCAXSH6KyOOWw==",
                    "referenceID": 2084,
                    "referenceName": "Zone",
                    "referenceString": "<Resource URI=\"/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 10.0.0.0-10.255.255.255\" ID=\"ML8022AABABCDTFpYAT3UdQ==\"/>",
                    "referenceType": 29,
                    "uri": "/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 10.0.0.0-10.255.255.255"
                },
                "timeZone": "Asia/Jerusalem",
                "version": "7.15.0.8295.0",
                "id": "3CgN77nEBABDaCRMDAaJaBw==",
                "name": "syslog_10525",
                "type": "syslog"
            },
            "concentratorDevices": {
                "mutable": true,
                "address": 174351988,
                "addressAsBytes": "CmRmdA==",
                "assetId": "4+ZGOMnEBABCDkWcZFgAOeA==",
                "assetLocalId": 17179869190,
                "assetName": "10.100.102.116",
                "macAddress": -9223372036854775808,
                "translatedAddress": -9223372036854775808,
                "zone": {
                    "id": "ML8022AABABCDTFpYAT3UdQ==",
                    "isModifiable": false,
                    "managerID": "UUQVDXEBABCAXSH6KyOOWw==",
                    "referenceID": 2084,
                    "referenceName": "Zone",
                    "referenceString": "<Resource URI=\"/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 10.0.0.0-10.255.255.255\" ID=\"ML8022AABABCDTFpYAT3UdQ==\"/>",
                    "referenceType": 29,
                    "uri": "/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 10.0.0.0-10.255.255.255"
                },
                "timeZone": "Asia/Jerusalem",
                "version": 0,
                "product": "SIEM Kit",
                "vendor": "CyberSIEM(R) Community"
            },
            "correlatedEventCount": 0,
            "device": {
                "mutable": true,
                "address": 174351988,
                "addressAsBytes": "CmRmdA==",
                "assetId": "4+ZGOMnEBABCDkWcZFgAOeA==",
                "assetLocalId": 17179869190,
                "assetName": "10.100.102.116",
                "macAddress": -9223372036854775808,
                "translatedAddress": -9223372036854775808,
                "zone": {
                    "id": "ML8022AABABCDTFpYAT3UdQ==",
                    "isModifiable": false,
                    "managerID": "UUQVDXEBABCAXSH6KyOOWw==",
                    "referenceID": 2084,
                    "referenceName": "Zone",
                    "referenceString": "<Resource URI=\"/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 10.0.0.0-10.255.255.255\" ID=\"ML8022AABABCDTFpYAT3UdQ==\"/>",
                    "referenceType": 29,
                    "uri": "/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 10.0.0.0-10.255.255.255"
                },
                "timeZone": "Asia/Jerusalem",
                "version": 0,
                "product": "SIEM Kit",
                "vendor": "CyberSIEM(R) Community"
            },
            "deviceCustomDate1": -9223372036854775808,
            "deviceCustomDate2": -9223372036854775808,
            "deviceCustomFloatingPoint1": 4.9E-324,
            "deviceCustomFloatingPoint2": 4.9E-324,
            "deviceCustomFloatingPoint3": 4.9E-324,
            "deviceCustomFloatingPoint4": 4.9E-324,
            "deviceCustomNumber1": -9223372036854775808,
            "deviceCustomNumber2": -9223372036854775808,
            "deviceCustomNumber3": -9223372036854775808,
            "deviceDirection": -2147483648,
            "deviceEventClassId": 100,
            "deviceProcessId": -2147483648,
            "deviceReceiptTime": 1595968655010,
            "deviceSeverity": "Unknown",
            "domainDate1": -9223372036854775808,
            "domainDate2": -9223372036854775808,
            "domainDate3": -9223372036854775808,
            "domainDate4": -9223372036854775808,
            "domainDate5": -9223372036854775808,
            "domainDate6": -9223372036854775808,
            "domainFp1": 4.9E-324,
            "domainFp2": 4.9E-324,
            "domainFp3": 4.9E-324,
            "domainFp4": 4.9E-324,
            "domainFp5": 4.9E-324,
            "domainFp6": 4.9E-324,
            "domainFp7": 4.9E-324,
            "domainFp8": 4.9E-324,
            "domainIpv4addr1": -9223372036854775808,
            "domainIpv4addr2": -9223372036854775808,
            "domainIpv4addr3": -9223372036854775808,
            "domainIpv4addr4": -9223372036854775808,
            "domainNumber1": -9223372036854775808,
            "domainNumber10": -9223372036854775808,
            "domainNumber11": -9223372036854775808,
            "domainNumber12": -9223372036854775808,
            "domainNumber13": -9223372036854775808,
            "domainNumber2": -9223372036854775808,
            "domainNumber3": -9223372036854775808,
            "domainNumber4": -9223372036854775808,
            "domainNumber5": -9223372036854775808,
            "domainNumber6": -9223372036854775808,
            "domainNumber7": -9223372036854775808,
            "domainNumber8": -9223372036854775808,
            "domainNumber9": -9223372036854775808,
            "endTime": 1595968655010,
            "eventAnnotation": {
                "auditTrail": "1,1595435564387,root,Queued,,,,\n",
                "flags": 0,
                "modificationTime": 1595968683168,
                "stage": {
                    "id": "R9MHiNfoAABCASsxbPIxG0g==",
                    "isModifiable": false,
                    "managerID": "UUQVDXEBABCAXSH6KyOOWw==",
                    "referenceID": 2209,
                    "referenceName": "Stage",
                    "referenceString": "<Resource URI=\"/All Stages/Queued\" ID=\"R9MHiNfoAABCASsxbPIxG0g==\"/>",
                    "referenceType": 34,
                    "uri": "/All Stages/Queued"
                },
                "stageUpdateTime": 1595968683168,
                "version": 1,
                "endTime": 1595968655010,
                "eventId": 120740877,
                "managerReceiptTime": 1595968683168
            },
            "eventId": 120740877,
            "finalDevice": {
                "mutable": true,
                "address": 174351988,
                "addressAsBytes": "CmRmdA==",
                "assetId": "4+ZGOMnEBABCDkWcZFgAOeA==",
                "assetLocalId": 17179869190,
                "assetName": "10.100.102.116",
                "macAddress": -9223372036854775808,
                "translatedAddress": -9223372036854775808,
                "zone": {
                    "id": "ML8022AABABCDTFpYAT3UdQ==",
                    "isModifiable": false,
                    "managerID": "UUQVDXEBABCAXSH6KyOOWw==",
                    "referenceID": 2084,
                    "referenceName": "Zone",
                    "referenceString": "<Resource URI=\"/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 10.0.0.0-10.255.255.255\" ID=\"ML8022AABABCDTFpYAT3UdQ==\"/>",
                    "referenceType": 29,
                    "uri": "/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 10.0.0.0-10.255.255.255"
                },
                "timeZone": "Asia/Jerusalem",
                "version": 0,
                "product": "SIEM Kit",
                "vendor": "CyberSIEM(R) Community"
            },
            "flexDate1": -9223372036854775808,
            "flexNumber1": -9223372036854775808,
            "flexNumber2": -9223372036854775808,
            "locality": 0,
            "managerId": -128,
            "managerReceiptTime": 1595968683168,
            "modelConfidence": 0,
            "name": "MailService Development",
            "originalAgent": {
                "mutable": true,
                "address": 174351991,
                "addressAsBytes": "CmRmdw==",
                "assetId": "4paH4P3EBABCSMnSiDweTZg==",
                "assetLocalId": 17179869193,
                "assetName": "linuxconn",
                "hostName": "linuxconn",
                "macAddress": 52229671306,
                "translatedAddress": -9223372036854775808,
                "zone": {
                    "id": "ML8022AABABCDTFpYAT3UdQ==",
                    "isModifiable": false,
                    "managerID": "UUQVDXEBABCAXSH6KyOOWw==",
                    "referenceID": 2084,
                    "referenceName": "Zone",
                    "referenceString": "<Resource URI=\"/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 10.0.0.0-10.255.255.255\" ID=\"ML8022AABABCDTFpYAT3UdQ==\"/>",
                    "referenceType": 29,
                    "uri": "/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 10.0.0.0-10.255.255.255"
                },
                "timeZone": "Asia/Jerusalem",
                "version": "7.15.0.8295.0",
                "id": "3CgN77nEBABDaCRMDAaJaBw==",
                "name": "syslog_10525",
                "type": "syslog"
            },
            "originator": "SOURCE",
            "persistence": -2147483648,
            "priority": 2,
            "relevance": 10,
            "sessionId": -9223372036854775808,
            "severity": 0,
            "source": {
                "mutable": true,
                "address": -9223372036854775808,
                "assetLocalId": -9223372036854775808,
                "macAddress": -9223372036854775808,
                "translatedAddress": -9223372036854775808,
                "port": -2147483648,
                "processId": -2147483648,
                "translatedPort": -2147483648,
                "userName": "King Dave"
            },
            "startTime": 1595968655010,
            "ttl": 10,
            "type": "BASE"
        }
    }
}
"""