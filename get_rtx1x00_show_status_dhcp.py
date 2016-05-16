#! /usr/bin/env python
#
# The MIT License (MIT)
#
# Copyright (c) 2016 Takeshi HASEGAWA <hasegaw@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import print_function

import argparse
import json
import os
import sys
import time


def get_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--all', action='store_true', help='size of lease')
    group.add_argument('--leased', action='store_true', help='# of lease used')
    group.add_argument('--usable', action='store_true',
                       help='# of lease available')
    parser.add_argument('file', help='Filename of the cached result')
    parser.add_argument('--by-percent', dest='pct',
                        action='store_true', help='show the value by percentage')
    return parser.parse_args()


def check_file_age(filename, age=3600 * 2):
    t = time.time()
    t_modified = os.stat(filename).st_mtime

    return (t - t_modified) < age


def percentage(value, total):
    return '%2.2f' % (value / total * 100)


def main():
    args = get_args()

    filename = args.file
    if not check_file_age(filename):
        # maybe the file is too old to read.
        print('Seems %s is too old.' % filename, file=sys.stderr)
        sys.exit(0)

    with open(filename) as data_file:
        data = json.load(data_file)

    if args.all:
        v = data.get('All', None)

    elif args.leased:
        v = data.get('Leased', None)

    elif args.usable:
        v = data.get('Usable', None)

    else:
        # not specified - human readable
        v = '%d of %d (%2.2f%%)' % (data['Leased'], data[
            'All'], data['Leased'] * 100 / data['All'])

    if isinstance(v, int) and args.pct:
        v = percentage(v, data['All'])

    if v is None:
        print('No data to output.', file=sys.stderr)
        sys.exit(1)

    print(v)
    sys.exit(0)

if __name__ == '__main__':
    main()
