#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib, json

class Tagstars(object):

    def __init__(self, args):

        self.username = args.username
        self.urlhandle = 'https://api.github.com/users/{}/starred'.format(self.username)

        try:
            self.resp = urllib.urlopen(self.urlhandle)
        except Exception, e:
                raise e

        self.resplist = json.loads(self.resp.read())

        if self.resplist:
            print 'Welcome, {}!'.format(self.username)
        else:
            print "Starred repositories not found from user '{}'".format(self.username)