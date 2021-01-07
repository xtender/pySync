# pySyncOracleStandby
Simple and absolutely configurable Sync service on Python for Oracle Standard edition standby

## Requirement

* Python 2.7+
* cx_Oracle

## Installation

Execute install.sh or

```bash
cp lib/systemd/system/pySyncOracleStandby.service /lib/systemd/system/pySyncOracleStandby.service
systemctl enable pySyncOracleStandby.service
systemctl status pySyncOracleStandby.service
```

### Install package:
```bash
# root or administrator permission may be required
pip install pySyncOracleStandby
```

## License

This project is licensed under the terms of the MIT license.
