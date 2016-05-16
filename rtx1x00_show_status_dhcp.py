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

import argparse
import json
import re
from subprocess import Popen, PIPE
import sys
import time


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('host', help='Hostname or IP address to talk to')
    parser.add_argument('passwd', help='Login password')
    parser.add_argument('file', help='Filename to cache the result')
    return parser.parse_args()


def run_expect(cmd):
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, close_fds=True)
    (child_stdout, child_stdin) = (p.stdout, p.stdin)

    lines = child_stdout.read().split('\r')

    r = {'time': int(time.time())}

    for l in lines:
        m = re.search('([A-Za-z]+): ([0-9]+)', l)
        if m:
            if m.group(1) in ['All', 'Leased', 'Usable']:
                r[m.group(1)] = int(m.group(2))

    return r


def main():
    args = get_args()
    cmd = './rtx1x00_show_status_dhcp.exp %s %s' % (args.host, args.passwd)
    r = run_expect(cmd)

    assert r['All'] > 0
    assert r['Leased'] >= 0
    assert r['Usable'] >= 0

    open(args.file, 'w').write(json.dumps(r) + '\n')
    sys.exit(0)

if __name__ == '__main__':
    main()
