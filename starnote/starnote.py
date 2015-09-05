#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import sys, json

class Starnote(object):

    def __init__(self, args):

        self.username = args.username
        self.req_url = 'https://api.github.com/users/%s' % self.username
        self.starred_file = 'starred.json'

        print "Updating %s's list of starred repositories..." % self.username
        self.res = requests.get(self.req_url)

        if self.res.status_code == 200:
            self.update_stars(self.username, self.starred_file)
        elif self.res.status_code == 403:
            print "Resquest denied, please wait and try again"
        else:
            print "User '%s' not found or invalid username" % self.username

    def update_stars(self, username, filename):

        self.total_pages = 1
        denied = False
        stars_url = 'https://api.github.com/users/{}/starred?per_page=100'.format(username)
        res = requests.get(stars_url)
        filebuf = res.json()

        if res.links:
            self.total_pages = int(res.links['last']['url'].split('&page=')[1])
            print "%d pages found (100 results per page)" % self.total_pages

            sys.stdout.write("Progress: [%s]" % (" " * self.total_pages))
            sys.stdout.flush()
            sys.stdout.write('\b' * (self.total_pages + 1))
            sys.stdout.write('=')

            for page in range(2, self.total_pages+1):
                p_url = (stars_url + '&page={1}').format(username, page)
                res = requests.get(p_url)

                if res.status_code == 403:
                    print "\nResquest denied, please wait and try again"
                    denied = True
                    break

                filebuf.extend(res.json())
                sys.stdout.write('=')
                sys.stdout.flush()

            sys.stdout.write('\n')
        else:
            print "Only 1 page found (100 results per page)"

        if not denied:
            with open(filename, 'w') as filehandle:
                json.dump(filebuf, filehandle, indent=2)

            print "Successfully updated and written in 'starred.json'"
            print len(filebuf)