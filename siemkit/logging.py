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


from traceback import format_exc
from datetime import datetime
import sys

settings = {
    'stdout': sys.__stdout__,
    'stderr': sys.__stderr__,
    'stdin': sys.__stdin__,
    'debug_mode': False
}


def format_exception(e):
    timestamp = datetime.now().isoformat()
    error_message = f"[{timestamp}] Exception: {type(e).__name__} \n{format_exc()}"
    return error_message


def format_message(msg):
    timestamp = datetime.now().isoformat()
    message = f"[{timestamp}] {msg}"
    return message


def print_exception(e):
    file = settings['stderr']
    print(format_exception(e), file=file)


def print_message(msg, file=None):

    if file is None:
        file = settings['stdout']

    print(format_message(msg), file=file)


def print_debug(msg, file=None, debug_mode=None):

    if file is None:
        file = settings['stdout']

    if debug_mode is None:
        debug_mode = settings['debug_mode']

    if debug_mode:
        print_message(f"DEBUG | {msg}", file=file)



