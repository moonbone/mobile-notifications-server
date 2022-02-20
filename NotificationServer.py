# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler, HTTPServer, test
import json
import time
import subprocess


class NotificationHTTPRequestHandler(BaseHTTPRequestHandler):

    blacklistApps = [u'com.google.android.googlequicksearchbox',
                     u'com.google.android.gm',
                     u'com.Slack',
                     u'com.google.android.apps.maps',
                     u'com.android.vending',
                     u'com.netflix.mediaclient',
                     u'com.agilebits.onepassword',
                     u'com.twitter.android',
                     u'com.pepper.pay',
                     u'com.google.android.apps.plus',
                     u'com.facebook.orca',
                     u'com.facebook.katana',
                     u'com.microsoft.skydrive',
                     u'com.microsoft.office.outlook',
                     u'com.google.intelligence.sense',
                     u'com.spotify.music',
                     u'com.google.android.apps.photos',
                     u'com.instagram.android',
                     u'com.android.systemui',
                     u'com.google.android.gms',
                     ]

    blacklistStrings = {k: None for k in blacklistApps}
    blacklistStrings[u'com.google.android.as'] = [u'Tap to ask your Assistant about this song']
    lastOKed = {}

    def __init__(self, request, client_address, _self):
        BaseHTTPRequestHandler.__init__(self, request,client_address, _self)



    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()


        d = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        print (time.ctime(), d)

        if d[u'app'] in NotificationHTTPRequestHandler.blacklistApps:
            return
        for blStr in NotificationHTTPRequestHandler.blacklistStrings.get(d[u'app'],[]):
            if blStr in d[u'title'] or blStr in d[u'text']:
                return
        if d[u'more'] and type(d[u'more']) == list and  d[u'text'] == d[u'more'][0]:
            del d[u'more'][0]
        if NotificationHTTPRequestHandler.lastOKed.get(d[u'app'], 0) + 10 < time.time():
            subprocess.call([u'swaynag', '-f', "Noto Color Emoji", '-m', '%s: %s' % ((d[u'app'] or '').split('.')[-1], (d[u'title'] or '')) + u" %s\t\t%s" % ((d[u'text'] or ''), '\n'.join((d[u'more']) or ''))])
            NotificationHTTPRequestHandler.lastOKed[d[u'app']] = time.time()


def main(HandlerClass = NotificationHTTPRequestHandler, ServerClass = HTTPServer):
    test(HandlerClass, ServerClass)



if __name__ == '__main__':
    main()
