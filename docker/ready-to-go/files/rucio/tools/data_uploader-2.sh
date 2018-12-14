#!/usr/bin/env bash

for f in {1..10};
    do
        new_file=MyFile.`uuidgen`
        echo $new_file
        dd if=/dev/zero of=$new_file bs=1024 count=1024;
        gfal-copy $new_file srm://srm.ndgf.org:8443/srm/managerv2?SFN=/atlas/disk/atlasdatadisk/piggy/MyScope/$new_file
        # curl --capath  /etc/grid-security/certificates/ -E $X509_USER_PROXY \
        # --fail --location \
        # --upload-file $new_file \
        # https://dav.ndgf.org/atlas/disk/atlasdatadisk/piggy/MyScope/
    done
