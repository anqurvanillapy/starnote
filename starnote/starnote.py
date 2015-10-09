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

        self.args = args
        self.cmd = args.cmd
        self.settings_filename = 'settings.json'

        if self.cmd == 'config':
            self.username = args.username
            try:
                pagination = int(input('> how many repos per page do you want? [15] '))

                if pagination <= 0:
                    pagination = 15
                    print "error: invalid input, setting 15 for pagination as default"
            except: # Exception, e:
                # raise e
                pagination = 15
                print "error: invalid input, setting 15 for pagination as default"

            settings = {
                "global_username": self.username,
                "pagination": pagination
            }

            try:
                with open(self.settings_filename, 'w') as filehandle:
                    json.dump(settings, filehandle, indent=2)
            except: # Exception, e:
                # raise e
                print "error: unable to write settings file"
                return
        else:
            try:
                with open(self.settings_filename, 'r') as filehandle:
                    settings = json.loads(filehandle.read())
                    self.username = settings['global_username']
            except: # Exception, e:
                # raise e
                print "error: unable to read settings file, try 'config' your username"
                return

        self.starred_file = '%s_starred.json' % self.username
        self.tagged_file = '%s_tagged.json' % self.username

        if self.cmd == 'update':
            print "updating %s's list of starred repositories..." % self.username
            self.update_stars(self.username, self.starred_file)
        elif self.cmd == 'list':
            self.list_stars(self.starred_file, args.listTags)
        elif self.cmd == 'add':
            self.add_tags(self.starred_file, args.tags, args.repos)
        elif self.cmd == 'remove':
            self.remove_tags(self.tagged_file, args.tags, args.repos)
        elif self.cmd == 'search':
            self.search_for_tags(self.tagged_file, args.tags, args.repos)
        elif self.cmd == 'book':
            self.launch_starnotebook(self.username, self.starred_file, self.tagged_file)

    def update_stars(self, username, filename):

        self.total_pages = 1
        stars_url = 'https://api.github.com/users/{}/starred?per_page=100'.format(username)

        try:
            filehandle = open(filename, 'r')
            local_latest = json.loads(filehandle.read())[0]['name']
            res = requests.get(stars_url)
            remote_latest = res.json()[0]['name']

            if local_latest == remote_latest:
                print "your local list of starred repositories is up-to-date"
                return
        except: # Exception, e:
            # raise e
            res = requests.get(stars_url)

        if res.status_code == 200:
            pass
        elif res.status_code == 404:
            print "error: user '%s' not found or invalid username" % username
            return
        else:
            print "error: bad request, please try again"
            return

        filebuf = res.json()

        if not filebuf:
            print "error: user '%s' has no starred repositories" % username
            return

        if res.links:
            self.total_pages = int(res.links['last']['url'].split('&page=')[1])
            print "%d pages found (100 results per page)" % self.total_pages
            print 'downloading list...'

            stdout.write("progress: [%s]" % (" " * self.total_pages))
            stdout.flush()
            stdout.write('\b' * (self.total_pages + 1))
            stdout.write('=')
            stdout.flush()

            for page in range(2, self.total_pages+1):
                p_url = (stars_url + '&page={1}').format(username, page)
                res = requests.get(p_url)

                if res.status_code == 403:
                    print "\nerror: resquest denied, please wait and try again"
                    return

                filebuf.extend(res.json())
                stdout.write('=')
                stdout.flush()

            stdout.write('\n')
        else:
            print "only 1 page found (100 results per page)"

        with open(filename, 'w') as filehandle:
            json.dump(filebuf, filehandle, indent=2)

        print "successfully updated and written in '%s_starred.json'" % username
        # print len(filebuf)

    def list_stars(self, filename, listTags=False):

        # Filename for starred_file
        if listTags:

            tagged_filename = filename.split('_starred.')[0] + '_tagged.json'

            try:
                with open(tagged_filename, 'r') as filehandle:
                    tagged_file = json.loads(filehandle.read())

                    if not tagged_file:
                        print "error: file '%s' is empty, try 'add' some tags" % tagged_filename
                        return

                    for item in list(reversed(tagged_file)):
                        name  = bcolors.OKBLUE + item['name'] + bcolors.ENDC
                        stars = bcolors.HEADER + unicode(item['stargazers_count']) + ' stars' + bcolors.ENDC
                        forks = bcolors.OKGREEN + unicode(item['forks_count']) + ' forks' + bcolors.ENDC
                        descp = item['description']
                        tags  = bcolors.WARNING
                        url   = bcolors.BOLD + item['html_url'] + bcolors.ENDC

                        for tag in item['tags']:
                            tags += '#' + tag + ' '

                        tags += bcolors.ENDC
                        print name, stars, forks, tags
                        print descp
                        print url
                        print
            except: # Exception, e:
                # raise e
                print "error: file '%s' not found, try 'add' some tags" % tagged_filename
        else:
            if not self.isStarredJSON(filename):
                return

            try:
                with open(filename, 'r') as filehandle:
                    starlist = json.loads(filehandle.read())

                    if not starlist:
                        print "error: file '%s' is empty, try 'update' your list" % filename
                        return

                    for item in list(reversed(starlist)):
                        name  = bcolors.OKBLUE + item['name'] + bcolors.ENDC
                        stars = bcolors.HEADER + unicode(item['stargazers_count']) + ' stars' + bcolors.ENDC
                        forks = bcolors.OKGREEN + unicode(item['forks_count']) + ' forks' + bcolors.ENDC
                        descp = item['description']
                        url   = bcolors.BOLD + item['html_url'] + bcolors.ENDC
                        print name, stars, forks
                        print descp
                        print url
                        print
            except: # Exception, e:
                # raise e
                print "error: file '%s' caused an error, try 'update' your list" % filename

    def add_tags(self, filename, tags, repos):

        if not self.isStarredJSON(filename):
            return

        if not tags or not repos:
            print "error: please specify tags and repos using '-t' and '-r' at the same time"
            return

        try:
            # Filename for starred_file
            with open(filename, 'r') as filehandle:
                starlist = json.loads(filehandle.read())
                starcatcher = []

                for repo in repos:
                    repos_not_found = True

                    for star in starlist:
                        if repo == star['name']:
                            starcatcher.append(star)
                            repos_not_found = False
                            break

                    if repos_not_found:
                        print "error: repo '%s' not found" % repo
        except: # Exception, e:
            # raise e
            print "error: file '%s' caused an error, try 'update' your list" % filename
            return

        tagged_filename = filename.split('_starred.')[0] + '_tagged.json'

        try:
            with open(tagged_filename, 'r') as filehandle:
                startagged = json.loads(filehandle.read())
        except: # Exception, e:
            # raise e
            startagged = []

        try:
            for item in starcatcher:
                stardict = {
                    "name": item['name'],
                    "description": item['description'],
                    "html_url": item['html_url'],
                    "stargazers_count": int(item['stargazers_count']),
                    "forks_count": int(item['forks_count']),
                    "tags": []
                }

                # Remove duplicates
                duplicated = False

                if startagged:
                    for tagged in startagged:
                        if stardict['name'] == tagged['name']:
                            for tag in tags:
                                tagged['tags'].append(tag)
                                tagged['tags'] = list(set(tagged['tags']))

                            duplicated = True
                            break

                if not duplicated:
                    for tag in tags:
                        stardict['tags'].append(tag)

                    startagged.append(stardict)
                    duplicated = False

                print "%d tags added to repo '%s'" % (len(tags), stardict['name'])

            with open(tagged_filename, 'w') as filehandle:
                filehandle.write(json.dumps(startagged, indent=2))
        except Exception, e:
            raise e

    def remove_tags(self, filename, tags, repos):

        if not self.isTaggedJSON(filename):
            return

        if not tags or not repos:
            print "error: please specify tags and repos using '-t' and '-r' at the same time"
            return

        try:
            # Filename for tagged_file
            with open(filename, 'r') as filehandle:
                tagged_starlist = json.loads(filehandle.read())

                for repo in repos:
                    remove_fail = True

                    for tag in tags:
                        for tagged in tagged_starlist:
                            if repo == tagged['name']:
                                if tag in tagged['tags']:
                                    tagged['tags'].remove(tag)
                                    remove_fail = False
                                    print "tag '%s' removed from '%s'" % (tag, tagged['name'])

                    if remove_fail:
                        print "error: cannot remove tag '%s' from '%s'" % (tag, repo)

                for tagged in tagged_starlist:
                    if not tagged['tags']:
                        print "warning: repo '%s' has no tags" % tagged['name']
                        tagged_starlist.remove(tagged)

            with open(filename, 'w') as filehandle:
                filehandle.write(json.dumps(tagged_starlist, indent=2))
        except: # Exception, e:
            # raise e
            print "error: file '%s' not found, try 'add' some tags" % filename

    def search_for_tags(self, filename, tags, repos):

        if not self.isTaggedJSON(filename):
            return

        try:
            # Filename for tagged_file
            with open(filename, 'r') as filehandle:
                tagged_starlist = json.loads(filehandle.read())

                if tags:
                    tags_not_found = True

                    for tag in tags:
                        print '---- %s ----' % (bcolors.WARNING + '#' + tag + bcolors.ENDC)

                        for tagged in tagged_starlist:
                            if tag in tagged['tags']:

                                name  = bcolors.OKBLUE + tagged['name'] + bcolors.ENDC
                                stars = bcolors.HEADER + unicode(tagged['stargazers_count']) + ' stars' + bcolors.ENDC
                                forks = bcolors.OKGREEN + unicode(tagged['forks_count']) + ' forks' + bcolors.ENDC
                                descp = tagged['description']
                                _tags = bcolors.WARNING
                                url   = bcolors.BOLD + tagged['html_url'] + bcolors.ENDC

                                for _tag in tagged['tags']:
                                    _tags += '#' + _tag + ' '

                                _tags += bcolors.ENDC
                                print name, stars, forks, _tags
                                print descp
                                print url
                                print
                                tags_not_found = False

                        if tags_not_found:
                            print "error: repo tagged '%s' not found" % tag
                elif repos:
                    repos_not_found = True

                    for repo in repos:
                        for tagged in tagged_starlist:
                            if repo in tagged['name']:

                                name  = bcolors.OKBLUE + tagged['name'] + bcolors.ENDC
                                stars = bcolors.HEADER + unicode(tagged['stargazers_count']) + ' stars' + bcolors.ENDC
                                forks = bcolors.OKGREEN + unicode(tagged['forks_count']) + ' forks' + bcolors.ENDC
                                descp = tagged['description']
                                tags = bcolors.WARNING
                                url   = bcolors.BOLD + tagged['html_url'] + bcolors.ENDC

                                for tag in tagged['tags']:
                                    tags += '#' + tag + ' '

                                tags += bcolors.ENDC
                                print name, stars, forks, tags
                                print descp
                                print url
                                print
                                repos_not_found = False

                        if repos_not_found:
                            print "error: repo named '%s' not found" % repo
        except: # Exception, e:
            # raise e
            print "error: file '%s' not found, try 'add' some tags" % filename

    def launch_starnotebook(self, username, starred_file, tagged_file):

        import starnotebook

        snb = starnotebook
        snb.init_user(username, starred_file, tagged_file)
        snb.run_starnotebook()

    def isStarredJSON(self, filename):

        if '_starred.' in filename:
            return True
        else:
            print "error: invalid filename '%s'" % filename
            return False

    def isTaggedJSON(self, filename):

        if '_tagged.' in filename:
            return True
        else:
            print "error: invalid filename '%s'" % filename
            return False