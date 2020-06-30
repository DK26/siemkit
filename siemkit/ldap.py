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


class UserAccountControlAttributes(Enum):

    # https://support.microsoft.com/en-us/help/305144/how-to-use-useraccountcontrol-to-manipulate-user-account-properties

    SCRIPT                          = 0x0001        # 1
    ACCOUNTDISABLE                  = 0x0002        # 2
    HOMEDIR_REQUIRED 	            = 0x0008        # 8
    LOCKOUT                         = 0x0010        # 16
    PASSWD_NOTREQD                  = 0x0020        # 32
    PASSWD_CANT_CHANGE              = 0x0040 	    # 64
    ENCRYPTED_TEXT_PWD_ALLOWED      = 0x0080 	    # 128
    TEMP_DUPLICATE_ACCOUNT          = 0x0100 	    # 256
    NORMAL_ACCOUNT                  = 0x0200 	    # 512
    INTERDOMAIN_TRUST_ACCOUNT 	    = 0x0800 	    # 2048
    WORKSTATION_TRUST_ACCOUNT 	    = 0x1000 	    # 4096
    SERVER_TRUST_ACCOUNT            = 0x2000 	    # 8192
    DONT_EXPIRE_PASSWORD 	        = 0x10000 	    # 65536
    MNS_LOGON_ACCOUNT 	            = 0x20000 	    # 131072
    SMARTCARD_REQUIRED 	            = 0x40000 	    # 262144
    TRUSTED_FOR_DELEGATION 	        = 0x80000 	    # 524288
    NOT_DELEGATED 	                = 0x100000 	    # 1048576
    USE_DES_KEY_ONLY 	            = 0x200000 	    # 2097152
    DONT_REQ_PREAUTH                = 0x400000 	    # 4194304
    PASSWORD_EXPIRED                = 0x800000 	    # 8388608
    TRUSTED_TO_AUTH_FOR_DELEGATION  = 0x1000000 	# 16777216
    PARTIAL_SECRETS_ACCOUNT 	    = 0x04000000  	# 67108864


class SAMAccountTypeAttributes(Enum):

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

