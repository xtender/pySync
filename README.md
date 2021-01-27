# pySyncOracleStandby
Simple and fully configurable Sync service on Python for Oracle Standard edition standby

## Requirement

* Python 2.7+
* cx_Oracle

## Installation

1. Copy config.cfg.example as config.cfg and configure it with own parameters

2. Execute install.sh or

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
