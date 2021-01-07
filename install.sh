#!/bin/bash

cp lib/systemd/system/pySyncOracleStandby.service /lib/systemd/system/pySyncOracleStandby.service
systemctl enable pySyncOracleStandby.service
systemctl status pySyncOracleStandby.service