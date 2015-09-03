#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from tagstars import Tagstars


def parse_arguments():

    parser = argparse.ArgumentParser(
        description='Tag your GitHub starred repositories')

    parser.add_argument(
        'username',
        metavar='username',
        action='store',
        help='specify your username'
        )

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    run_tagstars = Tagstars(args)