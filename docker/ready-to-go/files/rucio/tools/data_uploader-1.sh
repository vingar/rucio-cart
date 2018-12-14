#!/usr/bin/env bash

for f in {1..10};
    do
        new_file=MyFile.`uuidgen`
        echo $new_file
        dd if=/dev/zero of=$new_file bs=1024 count=1024;
        # echo 'Rucio upload'
        rucio upload $new_file  --rse NDGF-KERMIT --scope MyScope
        # echo 'Rucio add rule'
        rucio add-rule MyScope:$new_file 1 DESY-PROMETHEUS
    done
