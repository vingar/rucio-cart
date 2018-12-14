#!/usr/bin/env python

import argparse
import json
import logging
import getpass
import requests
import traceback
import urllib3
import os

from Queue import Queue
from threading import Thread

from sseclient import SSEClient

from rucio.client import Client

_DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

_LOGGER = logging.getLogger(__name__)

def _configure_logging():
    _LOGGER.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()

    formatter = logging.Formatter(_DEFAULT_LOG_FORMAT)
    ch.setFormatter(formatter)

    _LOGGER.addHandler(ch)


def get_parser():
    '''
    Method to return the argparse parser.
    '''
    parser = argparse.ArgumentParser(description='Sample dCache SSE consumer')
    parser.add_argument('--endpoint',
                        default="https://discordia.desy.de:3880/api/v1/events",
                        help="The events endpoint.  This should be a URL like 'https://frontend.example.org:3880/api/v1/events'.")
    # parser.add_argument('--user', metavar="NAME", default=getpass.getuser(),
    #                    help="The dCache username.  Defaults to the current user's name.")
    # parser.add_argument('--password', default=None,
    #                    help="The dCache password.  Defaults to prompting the user.")
    parser.add_argument('--inotify', default=None, metavar="PATH",
                        help="Subscribe to events on PATH.")
    parser.add_argument(
        '--proxy', dest='proxy',
        default=os.environ.get('X509_USER_PROXY', '/tmp/x509up_u' + str(os.getuid())),
        help='Client X509 proxy file.')
    return parser


def do_stuff(q, storage, rse, scope, proxy):

    rucio_client = Client()
    s = requests.Session()
    # s.auth = (user,pw)
    s.cert = proxy
    s.verify = False
    urllib3.disable_warnings()
    while True:
        try:
            name, new_file = q.get()
            response = s.get(new_file, headers={'Want-Digest': 'adler32'})
            adler32 = response.headers['Digest'].replace('adler32=', '')
            bytes = response.headers['Content-Length']
            replica  = {
                'scope': scope,
                'name': name,
                'pfn': new_file,
                'bytes': int(bytes),
                'adler32': adler32}

            rucio_client.add_replicas(
                rse='DESY-DISCORDIA',
                files=[replica])

            rucio_client.add_replication_rule(
                dids=[{'scope': scope, 'name': name}],
                account='root',
                copies=1,
                rse_expression=rse,
                grouping='NONE',
                weight=None,
                lifetime=None,
                locked=False)
            _LOGGER.info('Added replica and rule for file' + scope+ ':' + name)
        except:
            _LOGGER.error(traceback.format_exc())

        finally:
            q.task_done()


def _main():
    '''
    main function
    '''
    parser = get_parser()
    args = parser.parse_args()
    # user = vars(args).get("user")
    # pw = vars(args).get("password")
    proxy = vars(args).get("proxy")
    storage = 'http://discordia.desy.de:2880'
    scope = 'MyScope'
    rse = 'DESY-PROMETHEUS'
#    rse = 'DESY-DISCORDIA'
    # if not pw:
    #    pw = getpass.getpass("Please enter dCache password for user " + user + ": ")

    new_files = Queue(maxsize=0)
    worker = Thread(target=do_stuff, args=(new_files, storage, rse, scope, proxy))
    worker.setDaemon(True)
    worker.start()

    s = requests.Session()
    # s.auth = (user,pw)
    s.cert = proxy
    ## FIXME -- here we (in effect) disable all security from TLS.
    ##          This should be fixed by allowing the user to specify
    ##          an alternative trust-store
    s.verify = False
    urllib3.disable_warnings()

    response = s.post(vars(args).get("endpoint") + '/channels')
    channel = response.headers['Location']

    _LOGGER.info("Channel is {}".format(channel))

    path = vars(args).get("inotify")
    if path:
        r = s.post(format(channel) + "/subscriptions/inotify", json={"path" : path})
        watch = r.headers['Location']
        _LOGGER.info("Watch on {} is {}".format(path, watch))

    messages = SSEClient(channel, session=s)
    for msg in messages:
#        print "Event {}:".format(msg.id)
#        print "    event: {}".format(msg.event)
#        print "    data: {}".format(msg.data)
        data = json.loads(msg.data)
        if data['event']['mask'] == ['IN_ATTRIB']:
            # new file
            name = data['event']['name']
            new_file = storage + path + '/' + name
            _LOGGER.info('New file detected: ' + new_file)
            new_files.put((name, new_file))

if __name__ == '__main__':
    _configure_logging()
    _main()
