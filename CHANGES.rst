Changelog
=========

v0.3
----
- Fixed a re-scaling bug in the reservoir which would cause math overflow after a while
- Add some logging
- Rename counts to "total" for StatsD reporter because most copy-paste graphite config aggregates ".count$" via sum, not avg

v0.2
----
- fixed a major performance bug
- added support for py33

v0.1
----
- Initial release
