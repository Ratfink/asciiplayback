#!/usr/bin/env python2
# download_asciimation.py - Download animations from ASCIImator.net
# Copyright (c) 2013 Clayton G. Hobbs
# 
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import urllib, urlparse
from optparse import OptionParser

opt = OptionParser(usage='%prog [options] URL')

opt.add_option('-o', action='store', type='string', dest='output',
               help='Save to specified filename instead of the default')
opt.add_option('-v', action='store_true', dest='verbose',
               help="Say what's happening (default)")
opt.add_option('-q', action='store_false', dest='verbose', default=True,
               help='Give as little output as possible')

options, args = opt.parse_args()

url = args[0]
u = urlparse.urlparse(url)
try:
    clip_id = urlparse.parse_qs(u.query)['clip_id']
except KeyError:
    clip_id = u.path.split('/')[-1]
output = '%s.js'%clip_id[0] if not options.output else options.output
js_url = 'http://asciimator.net/ascii.files/%s.js' % clip_id[0]
if options.verbose:
    print 'Downloading %s...' % js_url
urllib.urlretrieve(js_url, output)

# TODO: Add ability to get animation title from HTML, use it in filename
# TODO: Add ability to download all animations by a given user
# TODO: Add ability to read comments from HTML perhaps
