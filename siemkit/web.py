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
from enum import Enum
from enum import IntEnum


class Protocol(str, Enum):

    HTTP    = 'http'
    HTTPS   = 'https'
    FTP     = 'ftp'

    def __str__(self):
        return self.value


class HttpInformationalCode(IntEnum):

    # REF: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

    # Informational Response: 1xx
    CONTINUE            = 100
    SWITCHING_PROTOCOLS = 101
    PROCESSING          = 102
    EARLY_HINTS         = 103


class HttpSuccessCode(IntEnum):

    # REF: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

    # Success: 2xx
    OK                              = 200
    CREATED                         = 201
    ACCEPTED                        = 202
    NON_AUTHORITATIVE_INFORMATION   = 203
    NO_CONTENT                      = 204
    RESET_CONTENT                   = 205
    PARTIAL_CONTENT                 = 206
    MULTI_STATUS                    = 207
    ALREADY_REPORTED                = 208
    IM_USED                         = 209


class HttpRedirectionCode(IntEnum):

    # REF: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

    # Redirection: 3xx
    MULTIPLE_CHOICES    = 300
    MOVED_PERMANENTLY   = 301
    FOUND               = 302
    SEE_OTHER           = 303
    NOT_MODIFIED        = 304
    USE_PROXY           = 305
    SWITCH_PROXY        = 306
    TEMPORARY_REDIRECT  = 307
    PERMANENT_REDIRECT  = 308


class HttpClientErrorCode(IntEnum):

    # REF: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

    # Client Errors: 4xx
    BAD_REQUEST                     = 400
    UNAUTHORIZED                    = 401
    PAYMENT_REQUIRED                = 402
    FORBIDDEN                       = 403
    NOT_FOUND                       = 404
    METHOD_NOT_ALLOWED              = 405
    NOT_ACCEPTABLE                  = 406
    PROXY_AUTHENTICATION_REQUIRED   = 407
    REQUEST_TIMEOUT                 = 408
    CONFLICT                        = 409
    GONE                            = 410
    LENGTH_REQUIRED                 = 411
    PRECONDITION_FAILED             = 412
    PAYLOAD_TOO_LARGE               = 413
    URI_TOO_LONG                    = 414
    UNSUPPORTED_MEDIA_TYPE          = 415
    RANGE_NOT_SATISFIABLE           = 416
    EXPECTATION_FAILED              = 417
    IM_A_TEAPOT                     = 418
    MISDIRECTED_REQUEST             = 421
    UNPROCESSABLE_ENTITY            = 422
    LOCKED                          = 423
    FAILED_DEPENDENCY               = 424
    TOO_EARLY                       = 425
    UPGRADE_REQUIRED                = 426
    PRECONDITION_REQUIRED           = 428
    TOO_MANY_REQUESTS               = 429
    REQUEST_HEADER_FIELDS_TOO_LARGE = 431
    UNAVAILABLE_FOR_LEGAL_REASONS   = 451


class HttpServerErrorCode(IntEnum):

    # REF: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

    # Server Errors: 5xx
    INTERNAL_SERVER_ERROR           = 500
    NOT_IMPLEMENTED                 = 501
    BAD_GATEWAY                     = 502
    SERVICE_UNAVAILABLE             = 503
    GATEWAY_TIMEOUT                 = 504
    HTTP_VERSION_NOT_SUPPORTED      = 505
    VARIANT_ALSO_NEGOTIATES         = 506
    INSUFFICIENT_STORAGE            = 507
    LOOP_DETECTED                   = 508
    NOT_EXTENDED                    = 510
    NETWORK_AUTHENTICATION_REQUIRED = 511


class HttpUnofficialCode(IntEnum):

    # REF: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

    # Unofficial Codes:
    CHECKPOINT                              = 103
    THIS_IS_FINE                            = 218
    PAGE_EXPIRED                            = 419
    METHOD_FAILURE                          = 420
    ENHANCE_YOUR_CALM                       = 420
    REQUEST_HEADER_FIELDS_TOO_LARGE         = 430
    BLOCKED_BY_WINDOWS_PARENTAL_CONTROLS    = 450
    INVALID_TOKEN                           = 498
    TOKEN_REQUIRED                          = 499
    BANDWIDTH_LIMIT_EXCEEDED                = 509
    INVALID_SSL_CERTIFICATE                 = 526
    SITE_IS_OVERLOADED                      = 529
    SITE_IS_FROZEN                          = 530
    NETWORK_READ_TIMEOUT_ERROR              = 598


class HttpIISCode(IntEnum):

    # REF: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

    # Microsoft Internet Information Services:
    LOGIN_TIME_OUT  = 440
    RETRY_WITH      = 449
    REDIRECT        = 451


class HttpNginxCode(IntEnum):

    # REF: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

    # nginx:
    NO_RESPONSE                     = 444
    REQUEST_HEADER_TOO_LARGE        = 494
    SSL_CERTIFICATE_ERROR           = 495
    SSL_CERTIFICATE_REQUIRED        = 496
    HTTP_REQUEST_SENT_TO_HTTPS_PORT = 497
    CLIENT_CLOSED_REQUEST           = 499


class HttpCloudflareCode(IntEnum):

    # REF: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

    # Cloudflare:
    WEB_SERVER_RETURNED_AN_UNKNOWN_ERROR    = 520
    WEB_SERVER_IS_DOWN                      = 521
    CONNECTION_TIMED_OUT                    = 522
    ORIGIN_IS_UNREACHABLE                   = 523
    A_TIMEOUT_OCCURRED                      = 524
    SSL_HANDSHAKE_FAILED                    = 525
    INVALID_SSL_CERTIFICATE                 = 526
    RAILGUN_ERROR                           = 527
    ERROR_FOLLOWS                           = 530


class HttpAWSElasticLoadBalancerCode(IntEnum):

    # REF: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

    # AWS Elastic Load Balancer:
    CLIENT_CLOSED_THE_CONNECTION_WITH_THE_LOAD_BALANCER_BEFORE_THE_IDLE_TIMEOUT_PERIOD_ELAPSED  = 460
    THE_LOAD_BALANCER_RECEIVED_AN_X_FORWARDED_FOR_REQUEST_HEADER_WITH_MORE_THAN_30_IP_ADDRESSES = 463











