#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import sys

class Starnote(object):

    def __init__(self, args):

        self.username = args.username
        self.req_url = 'https://api.github.com/users/%s' % self.username

        print "Updating %s's list of starred repositories..." % self.username

        try:
            self.res = requests.get(self.req_url)
        except Exception, e:
            raise e

        if self.res.status_code == 200:
            self.traverse_stars(self.username)
        elif self.res.status_code == 403:
            print "Resquest denied, please wait and try again"
        else:
            print "User '%s' not found or invalid username" % self.username

    def traverse_stars(self, username):

        self.total_pages = 1
        stars_url = 'https://api.github.com/users/{}/starred'.format(username)
        res = requests.get(stars_url)
        filebuf = res.json()

        if res.links:
            self.total_pages = int(res.links['last']['url'].split('?page=')[1])
            print "%d pages found" % self.total_pages

            sys.stdout.write("[%s]" % (" " * (self.total_pages - 1)))
            sys.stdout.flush()
            sys.stdout.write("\b" * (self.total_pages))

            for page in range(2, self.total_pages+1):

                p_url = (stars_url + '?page={1}').format(username, page)
                res = requests.get(p_url)
                filebuf.extend(res.json())

                sys.stdout.write('=')
                sys.stdout.flush()

            sys.stdout.write('\n')
        else:
            print "Only 1 page found"

        print len(filebuf)