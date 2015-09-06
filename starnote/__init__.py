#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, argparse
from starnote import Starnote

def init_path():

    path = os.getcwd()
    if path not in sys.path:
        sys.path.append(path)

def parse_arguments():

    parser = argparse.ArgumentParser(
        description='''Add your custom tags locally
        to your GitHub starred repositories'''
        )

    subparsers = parser.add_subparsers(
        help='Commands',
        dest='cmd'
        )

    # Update local list
    update_parser = subparsers.add_parser(
        'update',
        help='update local list of starred repositories'
        )

    update_parser.add_argument(
        'username',
        metavar='username',
        action='store',
        help='specify whose repos to update'
        )

    # List local starred repositories
    list_parser = subparsers.add_parser(
        'list',
        help='list your local starred repositories'
        )

    list_parser.add_argument(
        'username',
        metavar='username',
        action='store',
        help='specify whose repos to list'
        )

    list_parser.add_argument(
        '-t', '--tags',
        dest='listTags',
        action='store_true',
        default=False,
        help='list the tagged starred repositories'
        )

    # Add custom tags to starred repositories
    addtags_parser = subparsers.add_parser(
        'add',
        help='add custom tags to certain starred repositories'
        )

    addtags_parser.add_argument(
        'username',
        metavar='username',
        action='store',
        help='specify whose repos to add tags'
        )

    addtags_parser.add_argument(
        '-i', '--input',
        metavar='tag',
        dest='tags',
        action='store',
        nargs='+',
        help='names of tags, in your style'
        )

    addtags_parser.add_argument(
        '-o', '--output',
        metavar='repo',
        dest='repos',
        action='store',
        nargs='+',
        help='specify the repos your tags added to'
        )

    # Launch starnote book
    book_parser = subparsers.add_parser(
        'book',
        help='manage starred repositories in webpage'
        )

    book_parser.add_argument(
        'username',
        metavar='username',
        action='store',
        help='specify whose repos to access'
        )

    return parser.parse_args()

if __name__ == '__main__':
    init_path()
    args = parse_arguments()
    run_starnote = Starnote(args)