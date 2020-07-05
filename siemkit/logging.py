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


from traceback import extract_tb
from datetime import datetime
import sys


def format_exception(e):
    timestamp = datetime.now().isoformat()
    error_message = f"[{timestamp}] {type(e).__name__}: {e} \n{extract_tb(e)}"
    return error_message


def format_message(msg):
    timestamp = datetime.now().isoformat()
    message = f"[{timestamp}] {msg}"
    return message


def print_exception(e):
    print(format_exception(e), file=sys.stderr)


def print_message(msg, file=sys.stdout):
    print(format_message(msg), file=file)



