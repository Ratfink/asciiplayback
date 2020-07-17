#!/usr/bin/env python3
# download_asciimation.py - Download animations from ASCIImator.net
# Copyright (c) 2013, 2020 Clara Hobbs
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

import pathlib
import shutil
import urllib.parse
import urllib.request


def get_asciimation_id_from_url(url):
    """Returns the ID of the ASCIImation json from its web page

    Strongly assumes that the URL format is as it is in July 2020, when
    this was written.  It's changed in the past, but the current format
    looks nice enough that I expect it to stick around for a while.
    """
    # Parse and validate the URL
    u = urllib.parse.urlparse(url)
    if not u.netloc.endswith("asciimator.net"):
        raise ValueError("URL is not for asciimator.net")

    # Parse and validate the path in the URL
    p = pathlib.PurePosixPath(u.path).parts
    if (len(p) != 3 or p[0] != "/" or p[1] != "asciimation"
            or not p[2].isdigit()):
        raise ValueError("URL is not for an ASCIImation")

    return p[2]

def save_asciimation(url, output=None, verbose=False):
    """Download and save the specified ASCIImation"""
    am_id = get_asciimation_id_from_url(url)
    json_loc = "https://asciimator.net/animations/{}.json".format(am_id)
    if output is None:
        output = "{}.json".format(am_id)

    if verbose:
        print("Downloading {}...".format(json_loc))

    with urllib.request.urlopen(json_loc) as rsp, open(output, 'wb') as out:
        shutil.copyfileobj(rsp, out)


# TODO: Add ability to get animation title from HTML, use it in filename
# TODO: Add ability to download all animations by a given user
# TODO: Add ability to read comments from HTML perhaps


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
            description="Download animations from ASCIImator.net")

    parser.add_argument("url", type=str,
            help="URL of the webpage for the ASCIImation to download")
    parser.add_argument("-o", "--output", metavar="filename", type=str,
            help="Save to specified filename instead of the default")
    parser.add_argument("-v", "--verbose", action="store_true",
            help="Say what's happening")

    args = parser.parse_args()

    try:
        save_asciimation(args.url, args.output, args.verbose)
    except ValueError as e:
        parser.error(e)
