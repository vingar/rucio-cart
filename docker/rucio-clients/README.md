
```
export RUCIO_ACCOUNT={your account}
export X509_USER_CERT=~/.globus/usercert.pem
export X509_USER_KEY=~/.globus/userkey.pem
export RUCIO_AUTH_TYPE=x509_proxy
```

Then configure Rucio.




```
docker run \
-v $X509_USER_CERT:$X509_USER_CERT \
-v $X509_USER_KEY:$X509_USER_KEY \
-e X509_USER_CERT=$X509_USER_CERT \
-e X509_USER_KEY=$X509_USER_KEY \
-e RUCIO_ACCOUNT=$RUCIO_ACCOUNT \
-e RUCIO_AUTH_TYPE=$RUCIO_AUTH_TYPE \
-it -d --name rucio-clients rucio/rucio-clients
```
and:
```
docker exec -it rucio-clients /bin/bash
```

then:
```
 voms-proxy-init
 voms-proxy-info
 export X509_USER_PROXY=/tmp/x509up_u$(id -u)
 rucio ping
```
