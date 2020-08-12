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