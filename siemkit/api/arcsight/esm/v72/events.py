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

from typing import Tuple

from siemkit.api.arcsight.esm import ArcSightUri
from siemkit.api.arcsight.esm import ArcSightUriEnum


def init_event_ids(variables):

    event_ids = variables.get('event_ids')
    if event_ids is None:
        event_ids = []
    if isinstance(event_ids, int):
        event_ids = [event_ids]
    elif isinstance(event_ids, str):
        event_ids = [int(event_ids)]
    else:
        event_ids = list(event_ids)

    return event_ids


class GetSecurityEvents(ArcSightUri):

    def args(self, variables) -> Tuple[str, dict]:

        event_ids = init_event_ids(variables)

        start_millis = str(variables.get('start_millis', "-1"))
        end_millis = str(variables.get('end_millis', "-1"))

        return (
            '/www/manager-service/rest/SecurityEventService/getSecurityEvents',
            {
                'headers': {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                'method': 'POST',
                'json': {
                        "sev.getSecurityEvents": {
                            "sev.authToken": variables.get('token', ''),
                            "sev.ids": event_ids,
                            "sev.startMillis": start_millis,
                            "sev.endMillis": end_millis
                        }
                }
            }
        )


class EventsApiEnum(ArcSightUriEnum):
    GET_SECURITY_EVENTS = GetSecurityEvents()
