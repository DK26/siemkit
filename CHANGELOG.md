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
* All generators under `siemkit.random` were refactored from `compose` to `generate`
* Added ArcSight ESM API Manager methods:
    - `Esm.get_activelist_fields()`
    - `Esm.get_activelist_columns()`
    - `Esm.add_activelist_entries()`
* Passing columns to `remove_activelist_entries()` & `add_activelist_entries()` is only optional
    - Not providing the `_columns_order` field for an entry, will cause the API to automatically make a `get_activelist_columns()` call
* Improved ArcSight ESM API `retrieve_event_ids()` generator to be able to filter event types and retrieve recursively
* Fixed `siemkit.send.tcp` function
* Added `siemkit.event.Cef` aliases for `severity` & `deviceSeverity` are now both acceptable
* Added `siemkit.parse.boolean` new valid values for `True`:
    - `active`
    - `activated`
    - `include`
    - `included`
    - `enable`
    - `enabled`
    - `set`
    - `ready`
    - `allow`
    - `allowed`
    - `process`
    - `processed`
    - `add`
    - `added`
    - `run`
    - `running`
    - `go`
    - `start`
    - `able`
    - `capable`
    - `possible`
    - `can`
    - `permit`
    - `permitted`
    - `show`
    - `create`
    - `created`
    - `awake`
    - `wake`
    - `wakeup`
    - `wake-up`
    - `wake up`
    - `power`
    - `power-up`
    - `powerup`
    - `power up`
    - `alive`
    - `live`
    - `lives`
    - `contain`
    - `contained`
    - `insert`
    - `inserted`
    - `assign`
    - `assigned`
    - `import`
    - `imported`
    - `extract`
    - `extracted`
    - `+`
    - `v`
    - `x`
    - `promote`
    - `promoted`
    - `acknowledge`
    - `acknowledged`
    - `affirmative`
    - `happy`
    - `positive`
    - `select`
    - `selected`
* Changed: `siemkit.parse.boolean` is now using a `set` type for value testing instead of a `tuple`.

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