#!/bin/sh
journalctl --no-pager --all -o cat --grep='ca-certificates|update-ca-certificates|trust anchor|p11-kit|openssl'
