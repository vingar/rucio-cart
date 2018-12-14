#!/usr/bin/env python
# Authors:
# - Vincent Garonne <vgaronne@gmail.com>, 2017-2018

import os

from rucio.api.account import add_account
from rucio.api.identity import add_account_identity
from rucio.api.scope import add_scope
from rucio.api.did import add_did
from rucio.api.rse import add_rse
from rucio.db.sqla.util import build_database, create_root_account
from rucio.core.account_limit import set_account_limit
from rucio.core.rse import add_protocol, get_rse_id, add_rse_attribute

if __name__ == '__main__':
    # Create the Database and the root account
    build_database()
    create_root_account()
    add_account_identity('/CN=docker client', 'x509', 'root', 'test@rucio.com', issuer="root")
