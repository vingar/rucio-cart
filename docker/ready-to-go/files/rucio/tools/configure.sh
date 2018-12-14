#!/usr/bin/env bash

# Add source sites
rucio-admin rse add NDGF-PIGGY -i
rucio-admin rse add NDGF-KERMIT


# Add upload site
rucio-admin rse add DESY-DISCORDIA -i

# Add destination site
rucio-admin rse add DESY-PROMETHEUS

# Define the topology
rucio-admin rse add-distance --distance 1 --ranking 1 NDGF-PIGGY DESY-PROMETHEUS
rucio-admin rse add-distance --distance 1 --ranking 1 NDGF-KERMIT DESY-PROMETHEUS
rucio-admin rse add-distance --distance 1 --ranking 1 DESY-DISCORDIA DESY-PROMETHEUS

# Add protocol information for NDGF-PIGGY
# rucio-admin rse add-protocol --hostname dav.ndgf.org --scheme davs\
#      --prefix /atlas/disk/atlasdatadisk/\
#      --port 443 --impl rucio.rse.protocols.gfal.Default\
#      --domain-json '{"wan": {"read": 1, "write": 1, "delete": 1, "third_party_copy": 1}, "lan": {"read": 1, "write": 1, "delete": 1}}' \
#      NDGF-PIGGY

rucio-admin rse add-protocol --hostname srm.ndgf.org --scheme srm\
     --prefix /atlas/disk/atlasdatadisk/piggy/\
     --space-token ATLASDATADISK\
     --web-service-path /srm/managerv2?SFN=\
     --port 8443 --impl rucio.rse.protocols.gfal.Default\
     --domain-json '{"wan": {"read": 1, "write": 1, "delete": 1, "third_party_copy": 1}, "lan": {"read": 1, "write": 1, "delete": 1}}' \
     NDGF-PIGGY

# Add protocol information for NDGF-KERMIT
rucio-admin rse add-protocol --hostname srm.ndgf.org --scheme srm\
     --prefix /atlas/disk/atlasdatadisk/kermit/\
     --space-token ATLASDATADISK\
     --web-service-path /srm/managerv2?SFN=\
     --port 8443 --impl rucio.rse.protocols.gfal.Default\
     --domain-json '{"wan": {"read": 1, "write": 1, "delete": 1, "third_party_copy": 1}, "lan": {"read": 1, "write": 1, "delete": 1}}' \
     NDGF-KERMIT

# Add protocol information for destination DESY-PROMETHEUS
# rucio-admin rse add-protocol --hostname prometheus.desy.de --scheme davs\
#      --prefix /VOs/atlas/DATA/rucio/\
#      --port 443 --impl rucio.rse.protocols.gfal.Default\
#      --domain-json '{"wan": {"read": 1, "write": 1, "delete": 1, "third_party_copy": 1}, "lan": {"read": 1, "write": 1, "delete": 1}}' \
#      DESY-PROMETHEUS

rucio-admin rse add-protocol --hostname prometheus.desy.de --scheme srm\
     --prefix /VOs/atlas/DATA/rucio/\
     --space-token ATLASDATADISK\
     --web-service-path /srm/managerv2?SFN=\
     --port 8443 --impl rucio.rse.protocols.gfal.Default\
     --domain-json '{"wan": {"read": 1, "write": 1, "delete": 1, "third_party_copy": 1}, "lan": {"read": 1, "write": 1, "delete": 1}}' \
     DESY-PROMETHEUS

# Add protocol information for DESY-DISCORDIA
rucio-admin rse add-protocol --hostname discordia.desy.de --scheme srm\
      --prefix /home/garvin\
      --web-service-path /srm/managerv2?SFN=\
      --port 8443 --impl rucio.rse.protocols.gfal.Default\
      --domain-json '{"wan": {"read": 1, "write": 1, "delete": 1, "third_party_copy": 1}, "lan": {"read": 1, "write": 1, "delete": 1}}' \
      DESY-DISCORDIA

rucio-admin rse add-protocol --hostname discordia.desy.de --scheme http\
     --prefix /home/garvin\
     --port 2880 --impl rucio.rse.protocols.gfal.Default\
     --domain-json '{"wan": {"read": 1, "write": 1, "delete": 1, "third_party_copy": 1}, "lan": {"read": 1, "write": 1, "delete": 1}}' \
     DESY-DISCORDIA

# Define the FTS server for the Site
rucio-admin rse set-attribute --rse  NDGF-PIGGY --key fts  --value https://fts-rest:8446
rucio-admin rse set-attribute --rse  NDGF-KERMIT --key fts  --value https://fts-rest:8446
rucio-admin rse set-attribute --rse  DESY-PROMETHEUS --key fts  --value https://fts-rest:8446
rucio-admin rse set-attribute --rse  DESY-DISCORDIA --key fts  --value https://fts-rest:8446

rucio-admin rse set-attribute --rse  DESY-PROMETHEUS --key reaper  --value 1
rucio-admin rse set-attribute --rse  NDGF-KERMIT --key reaper  --value 1
rucio-admin rse set-attribute --rse  NDGF-PIGGY --key reaper  --value 1

# add scopes
rucio-admin scope add --scope MyScope --account root
rucio-admin scope add --scope tests --account root

# Set infinite quota to root account on NDGF-KERMIT, DESY-PROMETHEUS, DESY-DISCORDIA,
rucio-admin account set-limits root NDGF-KERMIT -1
rucio-admin account set-limits root DESY-PROMETHEUS -1
rucio-admin account set-limits root DESY-DISCORDIA -1

# Start the daemons
/usr/bin/python /usr/bin/supervisord -c /etc/supervisord.conf

# Install CAs + CRLs
# yum install -y ca-policy-lcg
# yum install -y ca-policy-egi-core
# yum install -y fetch-crl-3.0.19-1.el7.noarch
# /usr/sbin/fetch-crl -q -r 360
