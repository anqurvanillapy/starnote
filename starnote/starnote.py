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
        self.starred_file = '%s_starred.json' % self.username

        if self.cmd == 'update':
            print "Updating %s's list of starred repositories..." % self.username
            self.update_stars(self.username, self.starred_file)
        elif self.cmd == 'list':
            self.listTags = args.listTags
            self.list_stars(self.starred_file, self.listTags)
        elif self.cmd == 'add':
            self.tags = args.tags
            self.repos = args.repos
            self.add_tags(self.starred_file, self.tags, self.repos)

    def update_stars(self, username, filename):

        self.total_pages = 1
        denied = False
        stars_url = 'https://api.github.com/users/{}/starred?per_page=100'.format(username)

        try:
            filehandle = open(filename, 'r')
            local_latest = json.loads(filehandle.read())[0]['name']
            res = requests.get(stars_url)
            remote_latest = res.json()[0]['name']

            if local_latest == remote_latest:
                print "Your local list of starred repositories is up-to-date"
                return
        except:
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
            if not self.isStarredJSON(filename):
                return

            try:
                with open(filename, 'r') as filehandle:
                    starlist = json.loads(filehandle.read())

                    for item in list(reversed(starlist)):
                        name  = bcolors.OKBLUE + item['name'] + bcolors.ENDC
                        stars = bcolors.HEADER + unicode(item['stargazers_count']) + ' stars' + bcolors.ENDC
                        forks = bcolors.OKGREEN + unicode(item['forks_count']) + ' forks' + bcolors.ENDC
                        descp = item['description']
                        print name, stars, forks, descp
            except:
                print "File '%s' not found, try 'update' your list" % filename
                return

    def add_tags(self, filename, tags, repos):

        if not self.isStarredJSON(filename):
            return

        if not tags or not repos:
            print "Please specify tags and repos using '-i' and '-o' at the same time"
            return

        try:
            # Filename for starred_file
            with open(filename, 'r') as filehandle:
                starlist = []

                for item in repos:
                    print item
        except:
            print "File '%s' not found, try 'update' your list" % filename
            return

    def isStarredJSON(self, filename):

        if '_starred' in filename:
            return True
        else:
            print "Invalid filename '%s'" % filename
            return False