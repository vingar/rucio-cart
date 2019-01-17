#!/usr/bin/env bash

for f in {1..100};
    do
        new_file=File.`uuidgen`
        echo $new_file
        dd if=/dev/zero of=$new_file bs=1 count=1;
        # gfal-copy   --verbose  $new_file srm://preprod-srm.ndgf.org:8443/atlas/disk/atlasdatadisk/tarpool_ceph_uio_1/$new_file
        curl --capath  /etc/grid-security/certificates/  --cert $X509_USER_PROXY --key $X509_USER_PROXY   --cacert $X509_USER_PROXY   \
         --fail --location \
         --upload-file $new_file \
        https://preprod-srm.ndgf.org/atlas/disk/atlasdatadisk/tarpool_ceph_uio_1/
        rm  -f $new_file
    done
