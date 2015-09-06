#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from sys import stdout

class bcolors:

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Starnote(object):

    def __init__(self, args):

        self.cmd = args.cmd
        self.username = args.username
        self.req_url = 'https://api.github.com/users/%s' % self.username
        self.starred_file = '%s_starred.json' % self.username

        if self.cmd == 'update':

            print "Updating %s's list of starred repositories..." % self.username
            self.res = requests.get(self.req_url)

            if self.res.status_code == 200:
                self.update_stars(self.username, self.starred_file)
            elif self.res.status_code == 403:
                print "Resquest denied, please wait and try again"
            else:
                print "User '%s' not found or invalid username" % self.username
        elif self.cmd == 'list':
            self.listTags = args.listTags
            self.list_stars(self.starred_file, self.listTags)

    def update_stars(self, username, filename):

        self.total_pages = 1
        denied = False
        stars_url = 'https://api.github.com/users/{}/starred?per_page=100'.format(username)
        res = requests.get(stars_url)
        filebuf = res.json()

        if res.links:
            self.total_pages = int(res.links['last']['url'].split('&page=')[1])
            print "%d pages found (100 results per page)" % self.total_pages

            stdout.write("Progress: [%s]" % (" " * self.total_pages))
            stdout.flush()
            stdout.write('\b' * (self.total_pages + 1))
            stdout.write('=')

            for page in range(2, self.total_pages+1):
                p_url = (stars_url + '&page={1}').format(username, page)
                res = requests.get(p_url)

                if res.status_code == 403:
                    print "\nResquest denied, please wait and try again"
                    denied = True
                    break

                filebuf.extend(res.json())
                stdout.write('=')
                stdout.flush()

            stdout.write('\n')
        else:
            print "Only 1 page found (100 results per page)"

        if not denied:
            with open(filename, 'w') as filehandle:
                json.dump(filebuf, filehandle, indent=2)

            print "Successfully updated and written in '%s_starred.json'" % username
            # print len(filebuf)

    def list_stars(self, filename, listTags=False):

        if listTags:
            print 'Listing tagged repos!'
        else:
            if '_starred.json' not in filename:        
                print 'Invalid filename'
                return

            starlist = []

            try:
                with open(filename, 'r') as filehandle:
                    for item in json.loads(filehandle.read()):
                        starlist.append(item['name'])

                for i in starlist:
                    print bcolors.OKBLUE + i + bcolors.ENDC
            except:
                print "File '%s' not found, try 'update' your list" % filename