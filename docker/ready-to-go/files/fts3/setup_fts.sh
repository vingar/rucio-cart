#!/usr/bin/env bash

yum install -y mysql
mysql -u fts -h mysql --password=fts fts < /usr/share/fts-mysql/fts-schema-4.0.0.sql
