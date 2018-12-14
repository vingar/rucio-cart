#!/usr/bin/env bash

mkdir data

cd data

# Generate data, upload it and add replicate it
../tools/data_uploader-1.sh

cd ..

rm -rf data
