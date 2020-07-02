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

from enum import IntFlag
from enum import Enum
from typing import Generator


class UserAccountControlAttributes(IntFlag):

    # https://support.microsoft.com/en-us/help/305144/how-to-use-useraccountcontrol-to-manipulate-user-account-properties

    SCRIPT                          = 0x0001        # 1
    ACCOUNTDISABLE                  = 0x0002        # 2
    HOMEDIR_REQUIRED                = 0x0008        # 8
    LOCKOUT                         = 0x0010        # 16
    PASSWD_NOTREQD                  = 0x0020        # 32
    PASSWD_CANT_CHANGE              = 0x0040        # 64
    ENCRYPTED_TEXT_PWD_ALLOWED      = 0x0080        # 128
    TEMP_DUPLICATE_ACCOUNT          = 0x0100        # 256
    NORMAL_ACCOUNT                  = 0x0200        # 512
    INTERDOMAIN_TRUST_ACCOUNT       = 0x0800        # 2048
    WORKSTATION_TRUST_ACCOUNT       = 0x1000        # 4096
    SERVER_TRUST_ACCOUNT            = 0x2000        # 8192
    DONT_EXPIRE_PASSWORD            = 0x10000       # 65536
    MNS_LOGON_ACCOUNT               = 0x20000       # 131072
    SMARTCARD_REQUIRED              = 0x40000       # 262144
    TRUSTED_FOR_DELEGATION          = 0x80000       # 524288
    NOT_DELEGATED                   = 0x100000      # 1048576
    USE_DES_KEY_ONLY                = 0x200000      # 2097152
    DONT_REQ_PREAUTH                = 0x400000      # 4194304
    PASSWORD_EXPIRED                = 0x800000      # 8388608
    TRUSTED_TO_AUTH_FOR_DELEGATION  = 0x1000000     # 16777216
    PARTIAL_SECRETS_ACCOUNT         = 0x04000000    # 67108864


class SAMAccountTypeAttributes(IntFlag):

    # https://docs.microsoft.com/en-us/windows/win32/adschema/a-samaccounttype

    SAM_DOMAIN_OBJECT               = 0x0           # 0
    SAM_GROUP_OBJECT                = 0x10000000    # 268435456
    SAM_NON_SECURITY_GROUP_OBJECT   = 0x10000001    # 268435457
    SAM_ALIAS_OBJECT                = 0x20000000    # 536870912
    SAM_NON_SECURITY_ALIAS_OBJECT   = 0x20000001    # 536870913
    SAM_USER_OBJECT                 = 0x30000000    # 805306368
    SAM_NORMAL_USER_ACCOUNT         = 0x30000000    # 805306368
    SAM_MACHINE_ACCOUNT             = 0x30000001    # 805306369
    SAM_TRUST_ACCOUNT               = 0x30000002    # 805306370
    SAM_APP_BASIC_GROUP             = 0x40000000    # 1073741824
    SAM_APP_QUERY_GROUP             = 0x40000001    # 1073741825
    SAM_ACCOUNT_TYPE_MAX            = 0x7fffffff    # 2147483647


class GroupTypeAttributes(IntFlag):

    # https://docs.microsoft.com/en-us/windows/win32/adschema/a-grouptype

    CREATED_BY_SYSTEM   = 0x00000001    # 1
    GLOBAL_GROUP        = 0x00000002    # 2
    DOMAIN_LOCAL_GROUP  = 0x00000004    # 4
    UNIVERSAL_GROUP     = 0x00000008    # 8
    APP_BASIC           = 0x00000010    # 16
    APP_QUERY           = 0x00000020    # 32
    SECURITY_GROUP      = 0x80000000    # 2147483648  # if not a SECURITY_GROUP then it's a DISTRIBUTION_GROUP.


class InstanceTypeAttributes(IntFlag):

    # https://docs.microsoft.com/en-us/windows/win32/adschema/a-instancetype

    HEAD_OF_NAMING_CONTEXT                                      = 0x00000001  # 1
    REPLICA_NOT_INSTANTIATED                                    = 0x00000002  # 2
    OBJECT_IS_WRITEABLE                                         = 0x00000004  # 4
    NAMING_CONTEXT_ABOVE_THIS_ONE_IS_HELD                       = 0x00000008  # 8
    NAMING_CONTEXT_BEING_CONSTRUCTED_BY_REPLICATION_FIRST_TIME  = 0x00000010  # 16
    NAMING_CONTEXT_BEING_REMOVED_FROM_LOCAL_DSA                 = 0x00000020  # 32


class CommonQueries(Enum):

    # https://social.technet.microsoft.com/wiki/contents/articles/5392.active-directory-ldap-syntax-filters.aspx

    ALL_USER_OBJECTS                    = '(&(objectCategory=person)(objectClass=user))'
    ALL_COMPUTER_OBJECTS                = '(objectCategory=computer)'
    ALL_GROUP_OBJECTS                   = '(objectCategory=group)'
    ALL_ORGANIZATIONAL_UNIT_OBJECTS     = '(objectCategory=organizationalUnit)'
    ALL_DOMAIN_OBJECTS                  = '(objectCategory=domain)'

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value


def query_sam_account_type(sam_account_type: int) -> str:
    return f'(sAMAccountType={sam_account_type})'


def query_user_account_control_attribute(user_account_control_attribute: int) -> str:
    return f'(userAccountControl:1.2.840.113556.1.4.803:={user_account_control_attribute})'


def query_group_type(group_type: int) -> str:
    return f'(groupType:1.2.840.113556.1.4.803:={group_type})'


def dc_parts(domain: str) -> Generator[str, None, None]:
    for part in domain.split('.'):
        yield f'dc={part}'


def dc(domain: str) -> str:
    return ','.join(dc_parts(domain))
