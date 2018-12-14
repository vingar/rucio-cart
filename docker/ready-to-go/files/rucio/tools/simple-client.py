#!/usr/bin/env python


from sseclient import SSEClient
import requests
import urllib3
import getpass
import argparse

parser = argparse.ArgumentParser(description='Sample dCache SSE consumer')
parser.add_argument('--endpoint',
                    default="https://discordia.desy.de:3880/api/v1/events",
                    help="The events endpoint.  This should be a URL like 'https://frontend.example.org:3880/api/v1/events'.")
parser.add_argument('--user', metavar="NAME", default=getpass.getuser(),
                    help="The dCache username.  Defaults to the current user's name.")
parser.add_argument('--password', default=None,
                    help="The dCache password.  Defaults to prompting the user.")
parser.add_argument('--inotify', default=None, metavar="PATH",
                    help="Subscribe to events on PATH.")
args = parser.parse_args()

user = vars(args).get("user")
pw = vars(args).get("password")
if not pw:
    pw = getpass.getpass("Please enter dCache password for user " + user + ": ")

s = requests.Session()
s.auth = (user,pw)

## FIXME -- here we (in effect) disable all security from TLS.
##          This should be fixed by allowing the user to specify
##          an alternative trust-store
s.verify = False
urllib3.disable_warnings()

response = s.post(vars(args).get("endpoint") + '/channels')
channel = response.headers['Location']

print "Channel is {}".format(channel)

path = vars(args).get("inotify")
if path:
    r = s.post(format(channel) + "/subscriptions/inotify", json={"path" : path})
    print r.text
    watch = r.headers['Location']
    print "Watch on {} is {}".format(path, watch)

messages = SSEClient(channel, session=s)
for msg in messages:
    print "Event {}:".format(msg.id)
    print "    event: {}".format(msg.event)
    print "    data: {}".format(msg.data)

