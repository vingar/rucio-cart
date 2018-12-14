#!/usr/bin/env bash

rucio-admin subscription add \
    --account root\
    'FT data export' \
    '{"datatype": ["AOD"], "scope": ["tests"], "project": ["test"]}'\
    '[{"lifetime": 604800, "rse_expression": "DESY-DISCORDIA", "copies": 1, "grouping": "DATASET", "activity": "Functional Test"}]'\
    'suscription example'

rucio-automatix --run-once --input-file /opt/rucio/etc/automatix.json
