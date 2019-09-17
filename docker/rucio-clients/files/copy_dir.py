#!/usr/bin/env python
'''


'''

import argparse
import logging
import os
import random
import requests
import sys

from xml.parsers import expat

try:
    from urlparse import urlparse
except:
    from urllib.parse import urlparse


ROOTLOGGER = logging.getLogger('')
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)


ENDPOINTS = {
    'sara.nl': {'https': 'https://webdav.grid.surfsara.nl:2882',
                'davs': 'davs://webdav.grid.surfsara.nl:2882',
                'srm': 'srm://srm.grid.sara.nl:8443',
                'root': 'root://xrootd.grid.sara.nl:1094'},
    'ndgf.org': {'https': 'https://dav.ndgf.org:443',
                 'davs': 'davs://dav.ndgf.org:443',
                 'srm': 'srm://srm.ndgf.org:8443',
                 'root': 'root://srm.ndgf.org:1094'}}


def submit_transfer_to_fts(source_url, bytes, adler32, destination_url, proxy, fts_host,
                           protocol, dry_run=False):
    '''
    Submit transfers to FTS.

    '''
    # Convert URLs to the right protocol.
    for domain in ENDPOINTS:
        source_url = source_url.replace(ENDPOINTS[domain]['https'], ENDPOINTS[domain][protocol])
        destination_url = destination_url.replace(ENDPOINTS[domain]['https'], ENDPOINTS[domain][protocol])

    transfer_request = {'files': [{
        'sources': [source_url],
        'destinations': [destination_url],
        'filesize': bytes,
        'checksum': 'adler32:%s' % adler32}],
        'params': {'verify_checksum': True, 'overwrite': True}}


    if not dry_run:
        response = requests.post(
            '%s/jobs' % fts_host,
            json=transfer_request,
            cert=proxy,
            headers={'Content-Type': 'application/json'})
        LOGGER.info("Transfer from {} to {} has been submitted to FTS ({}).".format(source_url, destination_url, response.content))
    else:
        LOGGER.info("Transfer from {} to {} will be submitted to FTS.".format(source_url, destination_url))


class Parser:

    """ Parser to parse XML output for PROPFIND ."""

    def __init__(self):
        """ Initializes the object"""
        self._parser = expat.ParserCreate()
        self._parser.StartElementHandler = self.start
        self._parser.EndElementHandler = self.end
        self._parser.CharacterDataHandler = self.data
        self.hrefflag = 0
        self.href = ''
        self.status = 0
        self.size = 0
        self.dict = {}
        self.sizes = {}
        self.list = []

    def feed(self, data):
        """ Feed the parser with data"""
        self._parser.Parse(data, 0)

    def close(self):
        self._parser.Parse("", 1)
        del self._parser

    def start(self, tag, attrs):
        if tag == 'D:href' or tag == 'd:href':
            self.hrefflag = 1
        if tag == 'D:status' or tag == 'd:status':
            self.status = 1
        if tag == 'D:getcontentlength' or tag == 'd:getcontentlength':
            self.size = 1

    def end(self, tag):
        if tag == 'D:href' or tag == 'd:href':
            self.hrefflag = 0
        if tag == 'D:status' or tag == 'd:status':
            self.status = 0
        if tag == 'D:getcontentlength' or tag == 'd:getcontentlength':
            self.size = 0

    def data(self, data):
        if self.hrefflag:
            self.href = str(data)
            self.list.append(self.href)
        if self.status:
            self.dict[self.href] = data
        if self.size:
            self.sizes[self.href] = data


def get_parser():
    '''
    Get parser.
    '''
    oparser = argparse.ArgumentParser(
        prog=os.path.basename(sys.argv[0]),
        add_help=True)
    oparser.add_argument(
        '--debug',
        '-d',
        action='store_true',
        help='print debug messages to stderr.')
    oparser.add_argument(
        '--dry-run',
        action='store_true',
        help='show what would have been transferred.')
    oparser.add_argument(
        "--run-once",
        action="store_true",
        default=False,
        help='One iteration only')
    oparser.add_argument(
        '--ca-directory', dest='ca_directory', default='/etc/grid-security/certificates/',
        help='CA directory to verify peer against (SSL).')
    oparser.add_argument(
        '--x509_proxy', dest='x509_proxy',
        nargs='?', const=os.environ.get('X509_USER_PROXY', '/tmp/x509up_u' + str(os.getuid())),
        help='Client X509 proxy file.')
    oparser.add_argument(
        '--fts_host', dest="fts_host", default='https://fts.grid.surfsara.nl:8446',
        help="The FTS host name.")
    oparser.add_argument(
        '--destination', dest="destination", required=True,
        help="The destination directory URL.")
    oparser.add_argument(
        '--source', dest="source", required=True,
        help="The source directory URL.")
    return oparser


if __name__ == '__main__':
    oparser = get_parser()
    args = oparser.parse_args(sys.argv[1:])
    if args.debug:
        ROOTLOGGER.setLevel(logging.DEBUG)
    else:
        ROOTLOGGER.setLevel(logging.INFO)

    session = requests.Session()
    session.cert = args.x509_proxy
    session.verify = args.ca_directory
    fts_host = args.fts_host

    dir_url = args.source
    base_host = '%s://%s' % (urlparse(dir_url).scheme, urlparse(dir_url).netloc)
    src_dir = os.path.basename(os.path.normpath(dir_url))

    dest_url = args.destination
    base_dest_host = '%s://%s' % (urlparse(dest_url).scheme, urlparse(dest_url).netloc)

    LOGGER.debug(dir_url)
    response = session.request('PROPFIND', dir_url, headers={'Depth': '1'})
    parser = Parser()
    parser.feed(response.text)
    source_urls = []
    for file_name in parser.sizes:
        source_urls.append(base_host + file_name)
    parser.close()

    # source_urls.reverse()
    # random.shuffle(source_urls)
    protocol = random.choice(["srm", "davs"])
    # protocol = 'davs'

    for source_url in source_urls:
        src_file = os.path.basename(urlparse(source_url).path)
        destination_url = dest_url + '/' + src_dir + '/' + src_file
        response = session.head(source_url, headers={'Want-Digest': 'adler32'})
        adler32 = response.headers['Digest'].replace('adler32=', '')
        bytes = int(response.headers['Content-Length'])
#        LOGGER.info('About to submit a transfer from %s to %s with protocol %s', source_url, destination_url, protocol)
        submit_transfer_to_fts(source_url, bytes, adler32, destination_url,
                               session.cert, fts_host, protocol=protocol,
                               dry_run=args.dry_run)
        protocol = {'srm': 'davs', 'davs': 'srm'}.get(protocol)

        if args.run_once:
            break
