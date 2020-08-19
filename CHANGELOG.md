## Version 0.0.17-dev
* Added a random time generation `siemkit.random.time`
* Added a random time delta generation `siemkit.random.timedelta`
* Added a random time delta support for timedelta parsing `siemkit.parse.timedelta`
    - Examples of supported strings:
        - `from 1 day to 2 days`
        - `from 5 minutes to 1 hour`
        - `from every 2 minutes and 30 seconds to 5 minutes` 
* Added a random time support for time parsing `siemkit.parse.time`
    - Examples of supported strings:
        - `between yesterday and today`
        - `between yesterday and now`
        - `between 2 days ago and now`
        - `between 3 days ago and 2 days ago`
        - `between 1/1/2020 and 31/12/2023`
* Added parsing support for time range: `siemkit.parse.time_range` will produce a tuple of start and end time
* Re-imported sub-libraries for multi-layered APIs

## Version 0.0.16-dev
* Implemented prototype UDP listener
    - `siemkit.listen.udp`
* Implemented event Simulations:
    - `siemkit.simulate.cef.random_number()`
    - `siemkit.simulate.cef.fake_ip_scan()`
* Improved ArcSight ESM API:
    - SecurityEvent can optionally be pulled from any timestamp
* `send.py` functions can now accept Iterables.
    - `Generators` serve as a simulation set
    - Slightly improved efficiency
* Create the `generate.py` library:
    - Created `siemkit.generate.ip()` to generate a collection of IPs by range or amount.

## Version 0.0.15-dev
* Added ArcSight API
* Added SMTP support
* Improved `EventFormat` context manager
* Added `random.ip()` IP range
* Added `repeat` parameter to `send.py` functions
* `send.py` functions now accept any kind of object as payload & automatically convert to bytes
* A new, failure tolerant `tcp` implementation for the `net.py` library
* Logs now generate thread IDs as well
* New `html.py` library
* New `smtp.py` library