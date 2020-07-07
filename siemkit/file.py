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

import os
from datetime import datetime

builtin_open = open


def open(
        file,
        mode='r',
        buffering=-1,
        encoding=None,
        errors=None,
        newline=None,
        closefd=True,
        opener=None,
        utc=False,
        datetime_=None
):
    """
    Create a file stream addressing the file name with an attached timestamp.

    Example:

    ```
    with open('my_file_%y%m%d.txt', 'w') as fs:
        fs.write("Hello, world!")
    ```

    If this is executed in the 4th of July, 2020,
    the produced output file will then be `my_file_20200704.txt`.

    Optionally, the timestamp could be customized by passing a datetime object argument
    to the `datetime_` parameter.

    ```
    from datetime import datetime
    dt = datetime(day=4, month=7, year=1947)

    with open('my_file_%y%m%d.txt', 'w', datetime_=dt) as fs:
        fs.write("Hello, world!")
    ```

    The rest of the `open` function acts the same as Python's builtin version:

    Open file, optionally with time format, and return a stream.
    Raise OSError upon failure.

    file is either a text or byte string that may contain time format
    strings giving the name (and the path if the file isn't in the current
    working directory) of the file to be opened or an integer file
    descriptor of the file to be wrapped. (If a file descriptor is given,
    it is closed when the returned I/O object is closed, unless closefd is
    set to False.)

    mode is an optional string that specifies the mode in which the file
    is opened. It defaults to 'r' which means open for reading in text
    mode.  Other common values are 'w' for writing (truncating the file if
    it already exists), 'x' for creating and writing to a new file, and
    'a' for appending (which on some Unix systems, means that all writes
    append to the end of the file regardless of the current seek position).
    In text mode, if encoding is not specified the encoding used is platform
    dependent: locale.getpreferredencoding(False) is called to get the
    current locale encoding. (For reading and writing raw bytes use binary
    mode and leave encoding unspecified.) The available modes are:

    ========= ===============================================================
    Character Meaning
    --------- ---------------------------------------------------------------
    'r'       open for reading (default)
    'w'       open for writing, truncating the file first
    'x'       create a new file and open it for writing
    'a'       open for writing, appending to the end of the file if it exists
    'b'       binary mode
    't'       text mode (default)
    '+'       open a disk file for updating (reading and writing)
    'U'       universal newline mode (deprecated)
    ========= ===============================================================

    The default mode is 'rt' (open for reading text). For binary random
    access, the mode 'w+b' opens and truncates the file to 0 bytes, while
    'r+b' opens the file without truncation. The 'x' mode implies 'w' and
    raises an `FileExistsError` if the file already exists.

    Python distinguishes between files opened in binary and text modes,
    even when the underlying operating system doesn't. Files opened in
    binary mode (appending 'b' to the mode argument) return contents as
    bytes objects without any decoding. In text mode (the default, or when
    't' is appended to the mode argument), the contents of the file are
    returned as strings, the bytes having been first decoded using a
    platform-dependent encoding or using the specified encoding if given.

    'U' mode is deprecated and will raise an exception in future versions
    of Python.  It has no effect in Python 3.  Use newline to control
    universal newlines mode.

    buffering is an optional integer used to set the buffering policy.
    Pass 0 to switch buffering off (only allowed in binary mode), 1 to select
    line buffering (only usable in text mode), and an integer > 1 to indicate
    the size of a fixed-size chunk buffer.  When no buffering argument is
    given, the default buffering policy works as follows:

    * Binary files are buffered in fixed-size chunks; the size of the buffer
      is chosen using a heuristic trying to determine the underlying device's
      "block size" and falling back on `io.DEFAULT_BUFFER_SIZE`.
      On many systems, the buffer will typically be 4096 or 8192 bytes long.

    * "Interactive" text files (files for which isatty() returns True)
      use line buffering.  Other text files use the policy described above
      for binary files.

    encoding is the name of the encoding used to decode or encode the
    file. This should only be used in text mode. The default encoding is
    platform dependent, but any encoding supported by Python can be
    passed.  See the codecs module for the list of supported encodings.

    errors is an optional string that specifies how encoding errors are to
    be handled---this argument should not be used in binary mode. Pass
    'strict' to raise a ValueError exception if there is an encoding error
    (the default of None has the same effect), or pass 'ignore' to ignore
    errors. (Note that ignoring encoding errors can lead to data loss.)
    See the documentation for codecs.register or run 'help(codecs.Codec)'
    for a list of the permitted encoding error strings.

    newline controls how universal newlines works (it only applies to text
    mode). It can be None, '', '\n', '\r', and '\r\n'.  It works as
    follows:

    * On input, if newline is None, universal newlines mode is
      enabled. Lines in the input can end in '\n', '\r', or '\r\n', and
      these are translated into '\n' before being returned to the
      caller. If it is '', universal newline mode is enabled, but line
      endings are returned to the caller untranslated. If it has any of
      the other legal values, input lines are only terminated by the given
      string, and the line ending is returned to the caller untranslated.

    * On output, if newline is None, any '\n' characters written are
      translated to the system default line separator, os.linesep. If
      newline is '' or '\n', no translation takes place. If newline is any
      of the other legal values, any '\n' characters written are translated
      to the given string.

    If closefd is False, the underlying file descriptor will be kept open
    when the file is closed. This does not work when a file name is given
    and must be True in that case.

    A custom opener can be used by passing a callable as *opener*. The
    underlying file descriptor for the file object is then obtained by
    calling *opener* with (*file*, *flags*). *opener* must return an open
    file descriptor (passing os.open as *opener* results in functionality
    similar to passing None).

    open() returns a file object whose type depends on the mode, and
    through which the standard file operations such as reading and writing
    are performed. When open() is used to open a file in a text mode ('w',
    'r', 'wt', 'rt', etc.), it returns a TextIOWrapper. When used to open
    a file in a binary mode, the returned class varies: in read binary
    mode, it returns a BufferedReader; in write binary and append binary
    modes, it returns a BufferedWriter, and in read/write mode, it returns
    a BufferedRandom.

    It is also possible to use a string or bytearray as a file for both
    reading and writing. For strings StringIO can be used like a file
    opened in a text mode, and for bytes a BytesIO can be used like a file
    opened in a binary mode.

    :param file: A string representing the file name or full path.
                    May contain strftime time format strings
                    ("strftime() and strptime() Format Codes").

    Source: https://docs.python.org/3/library/datetime.html
    ========= ===============================================================
    Directive Meaning
    --------- ---------------------------------------------------------------
    %a       	Weekday as locale's abbreviated name.

                Example:

                    Sun, Mon, ..., Sat (en_US);
                    So, Mo, ..., Sa (de_DE)
    --------- ---------------------------------------------------------------
    %A       	Weekday as locale's full name.

                Example:

                    Sunday, Monday, ..., Saturday (en_US);
                    Sonntag, Montag, ..., Samstag (de_DE)
    --------- ---------------------------------------------------------------
    %w       	Weekday as a decimal number, where 0 is Sunday
                 and 6 is Saturday.

                Example:

                    0, 1, ..., 6
    --------- ---------------------------------------------------------------
    %d       	Day of the month as a zero-padded decimal number.

                Example:

                    01, 02, ..., 31
    --------- ---------------------------------------------------------------
    %b       	Month as locale's abbreviated name.

                Example:

                    Jan, Feb, ..., Dec (en_US);
                    Jan, Feb, ..., Dez (de_DE)
    --------- ---------------------------------------------------------------
    %B       	Month as locale's full name.

                Example:

                    January, February, ..., December (en_US);
                    Januar, Februar, ..., Dezember (de_DE)
    --------- ---------------------------------------------------------------
    %m       	Month as a zero-padded decimal number.

                Example:

                    01, 02, ..., 12
    --------- ---------------------------------------------------------------
    %y       	Year without century as a zero-padded decimal number.

                Example:

                    00, 01, ..., 99
    --------- ---------------------------------------------------------------
    %Y       	Year with century as a decimal number.

                Example:

                    0001, 0002, ..., 2013, 2014, ..., 9998, 9999
    --------- ---------------------------------------------------------------
    %H       	Hour (24-hour clock) as a zero-padded decimal number.

                Example:

                    00, 01, ..., 23
    --------- ---------------------------------------------------------------
    %I       	Hour (12-hour clock) as a zero-padded decimal number.

                Example:

                    01, 02, ..., 12
    --------- ---------------------------------------------------------------
    %p       	Locale's equivalent of either AM or PM.

                Example:

                    AM, PM (en_US);
                    am, pm (de_DE)
    --------- ---------------------------------------------------------------
    %M       	Minute as a zero-padded decimal number.

                Example:

                    00, 01, ..., 59
    --------- ---------------------------------------------------------------
    %S       	Second as a zero-padded decimal number.

                Example:

                    00, 01, ..., 59
    --------- ---------------------------------------------------------------
    %f       	Microsecond as a decimal number, zero-padded on the left.

                Example:

                    000000, 000001, ..., 999999
    --------- ---------------------------------------------------------------
    %z       	UTC offset in the form ±HHMM[SS[.ffffff]] (empty string if
                 the object is naive).

                Example:

                    (empty), +0000, -0400, +1030, +063415, -030712.345216
    --------- ---------------------------------------------------------------
    %Z       	Time zone name (empty string if the object is naive).

                Example:

                    (empty), UTC, EST, CST
    --------- ---------------------------------------------------------------
    %j       	Day of the year as a zero-padded decimal number.

                Example:

                    001, 002, ..., 366
    --------- ---------------------------------------------------------------
    %U       	Week number of the year (Sunday as the first day of the week)
                 as a zero padded decimal number. All days in a new year
                 preceding the first Sunday are considered to be in week 0.

                Example:

                    00, 01, ..., 53
    --------- ---------------------------------------------------------------
    %W       	Week number of the year (Monday as the first day of the week)
                 as a decimal number. All days in a new year preceding the
                 first Monday are considered to be in week 0.

                Example:

                    00, 01, ..., 53
    --------- ---------------------------------------------------------------
    %c       	Locale's appropriate date and time representation.

                Example:

                    Tue Aug 16 21:30:00 1988 (en_US);
                    Di 16 Aug 21:30:00 1988 (de_DE)
    --------- ---------------------------------------------------------------
    %x       	Locale's appropriate date representation.

                Example:

                    08/16/88 (None);
                    08/16/1988 (en_US);
                    16.08.1988 (de_DE)
    --------- ---------------------------------------------------------------
    %X       	Locale's appropriate time representation.

                Example:

                    21:30:00 (en_US);
                    21:30:00 (de_DE)
    --------- ---------------------------------------------------------------
    %%       	A literal '%' character.

                Example:

                    %
    ========= ===============================================================

    Several additional directives not required by the C89 standard are
     included for convenience. These parameters all correspond to ISO 8601
     date values.

    ========= ===============================================================
    Directive Meaning
    --------- ---------------------------------------------------------------
    %G       	ISO 8601 year with century representing the year that
                 contains the greater part of the ISO week (%V).

                Example:

                    0001, 0002, ..., 2013, 2014, ..., 9998, 9999
    --------- ---------------------------------------------------------------
    %u       	ISO 8601 weekday as a decimal number where 1 is Monday.

                Example:

                    1, 2, ..., 7
    --------- ---------------------------------------------------------------
    %V      	ISO 8601 week as a decimal number with Monday as the first
                 day of the week. Week 01 is the week containing Jan 4.

                Example:

                    01, 02, ..., 53
    ========= ===============================================================

    :param utc: If True, the time format of the file name will based
                    on current UTC time.

                Notice: This parameter is ignored if a `datetime_`
                         argument is given.

    :param datetime_: A datetime object to format the file name by.
                        By default, a new datetime is generated
                         with a current time.
    """

    # ToDo: Replace with time.to_format() -> add tz
    if isinstance(datetime_, datetime):
        dt = datetime_
    elif utc:
        dt = datetime.utcnow()
    else:
        dt = datetime.now()

    if 'w' in mode or 'a' in mode:
        directory_path = os.path.dirname(file)
        if directory_path:
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)

        file = dt.strftime(file)

    return builtin_open(
        file,
        mode=mode,
        buffering=buffering,
        encoding=encoding,
        errors=errors,
        newline=newline,
        closefd=closefd,
        opener=opener,
    )


def rotate():
    pass
