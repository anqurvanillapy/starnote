#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

class Starnote(object):

    def __init__(self, args):

        self.username = args.username
        self.req_url = 'https://api.github.com/users/{}/starred'.format(self.username)

        print "Updating {}'s list of starred repositories...".format(self.username)

        try:
            self.resp = requests.get(self.req_url)
        except Exception, e:
            raise e

        self.respjson = self.resp.json()

        if isinstance(self.respjson, list):
            if self.respjson:
                self.traverse_stars(self.respjson)
            else:
                print "User '{}' has no starred repositories".format(self.username)
        elif isinstance(self.respjson, dict):
            print "User '{}' not found or invalid username".format(self.username)
        else:
            print "Bad request but still cool, sir"

    def traverse_stars(self, starlist):

        for item in starlist:
            print item['name']