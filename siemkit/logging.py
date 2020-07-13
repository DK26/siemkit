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
from .file import open
from .time import to_format
import sys

settings = {
    'stdout': sys.stdout,
    'stderr': sys.stderr,
    'stdin': sys.stdin,
    'stddebug': sys.stdout,
    'debug_mode': False,
    'dump_file_name': 'dump_%d%m%Y-%H%M%S.log',
    'debug_dump_file_name': 'debug_dump_%d%m%Y-%H%M%S.log'
}

builtin_print = print


def print(*args, sep=' ', end='\n', file=None):

    if file is None:
        file = settings['stdout']

    timestamp = datetime.now().isoformat()
    builtin_print(f'[{timestamp}]', *args, sep=sep, end=end, file=file)


def format_exception(e):
    timestamp = datetime.now().isoformat()
    error_message = f"[{timestamp}] EXCEPTION | {type(e).__name__} \n{format_exc()}"
    return error_message


def format_message(msg):
    timestamp = datetime.now().isoformat()
    message = f"[{timestamp}] {msg}"
    return message


def print_exception(e):
    file = settings['stderr']
    builtin_print(format_exception(e), file=file)


def print_message(msg, file=None):

    if file is None:
        file = settings['stdout']

    builtin_print(format_message(msg), file=file)


def print_debug(msg, file=None, debug_mode=None):

    if debug_mode is None:
        debug_mode = settings['debug_mode']

    if debug_mode:

        if file is None:
            file = settings['stdout']

        print_message(f"DEBUG | {msg}", file=file)


def dump_debug(msg, payload, file=None, dump_file_name=None, debug_mode=None):

    if debug_mode is None:
        debug_mode = settings['debug_mode']

    if debug_mode:

        if file is None:
            file = settings['stdout']

        if dump_file_name is None:
            dump_file_name = settings['debug_dump_file_name']

        dump_file_name = to_format(format_=dump_file_name)
        print_message(f"DEBUG | DUMP | {msg}: '{dump_file_name}'", file=file)
        with open(dump_file_name, 'w', encoding='utf-8', errors='ignore') as fs:
            fs.write(format_message(f"DEBUG | DUMP | {msg}: \n{payload}"))


def dump(msg, payload, file=None, dump_file_name=None):

    if file is None:
        file = settings['stdout']

    if dump_file_name is None:
        dump_file_name = settings['dump_file_name']

    dump_file_name = to_format(format_=dump_file_name)
    print_message(f"DUMP | {msg}: '{dump_file_name}'", file=file)
    with open(dump_file_name, 'w', encoding='utf-8', errors='ignore') as fs:
        fs.write(format_message(f"DUMP | {msg}: \n{payload}"))
