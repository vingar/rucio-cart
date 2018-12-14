#!/usr/bin/env bash

# Generate and upload data
mkdir data
cd data

# Generate data, upload it and add replicate it
../tools/data_uploader-2.sh

# Generate the list of files
../tools/list-files > ../tools/replicas.csv

# bulk register replicas on source site
# Replicas are in ../tools/replicas.csv
/opt/rucio/tools/bulk_register_replicas

# Setup the replication
/opt/rucio/tools/bulk_register_rules

# Cleanup
cd ..

rm -rf data

#


