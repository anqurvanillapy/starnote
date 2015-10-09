#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO:
#   1. Add fuzzy finder to `-t` and `-r` arguments
#   2. Collect the err msgs to a class

import os, sys, argparse
import starnote

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

    # Configure username
    config_parser = subparsers.add_parser(
        'config',
        help='configure your username'
        )

    config_parser.add_argument(
        'username',
        metavar='username',
        action='store',
        help='specify whose repos to manage'
        )

    # Update local list
    update_parser = subparsers.add_parser(
        'update',
        help='update local list of starred repositories'
        )

    # List local starred repositories
    list_parser = subparsers.add_parser(
        'list',
        help='list your local starred repositories'
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
        '-t', '--tags',
        metavar='tag',
        dest='tags',
        action='store',
        nargs='+',
        help='names of tags, in your style'
        )

    addtags_parser.add_argument(
        '-r', '--repos',
        metavar='repo',
        dest='repos',
        action='store',
        nargs='+',
        help='specify the repos your tags added to'
        )

    # Remove custom tags from starred repositories
    removetags_parser = subparsers.add_parser(
        'remove',
        help='remove custom tags from starred repositories'
        )

    removetags_parser.add_argument(
        '-t', '--tags',
        metavar='tag',
        dest='tags',
        action='store',
        nargs='+',
        help='names of tags you want to remove'
        )

    removetags_parser.add_argument(
        '-r', '--repos',
        metavar='repo',
        dest='repos',
        action='store',
        nargs='+',
        help='specify the repos to remove tags'
        )

    # Search for custom tags or repositories
    search_parser = subparsers.add_parser(
        'search',
        help='search for tags or repositories'
        )

    kwd_parser = search_parser.add_mutually_exclusive_group()

    kwd_parser.add_argument(
        '-t', '--tags',
        metavar='tag',
        dest='tags',
        action='store',
        nargs='+',
        help='names of tags you want to search for'
        )

    kwd_parser.add_argument(
        '-r', '--repos',
        metavar='repo',
        dest='repos',
        action='store',
        nargs='+',
        help='specify the repos to search for'
        )

    # Launch starnote book
    book_parser = subparsers.add_parser(
        'book',
        help='manage starred repositories in webpage'
        )

    return parser.parse_args()

if __name__ == '__main__':
    init_path()
    args = parse_arguments()
    run_starnote = starnote.Starnote(args)