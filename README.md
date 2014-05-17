# ASCIIPlayback

    yo waddup                                 |
        /                       |/            |
      \O-     \ /       ='_     O-    o   o.o |
       %\      X    #   /!     /|'   /A\ / a >|
      / \     /@\ "|"|"  |>    / \ "|"|"  /|  |
    """""""""""""""""""""""""""""""""""""""""""

ASCIIPlayback is a program which plays files from
[ASCIImator](http://asciimator.net/).  It depends on Python 2 (tested with
2.7.6) and Pygame (tested with 1.9.1).  ASCIIPlayback is licensed under the MIT
license; see `LICENSE` for details.

## Usage

### Downloading

ASCIImations are currently downloaded by download\_asciimation.py, which is
used as follows:

    $ ./download_asciimation.py URL

where URL is the URL of the page you'd view in order to watch the ASCIImation
in your web browser.  For instance, to download
[Intelligence (1)](http://asciimator.net/asciimation/7676), the command would
be this:

    $ ./download_asciimation.py http://asciimator.net/asciimation/7676

The default filename is the number of the ASCIImation, but this can be changed
using the -o option.

### Playing

Once an ASCIImation has been downloaded, it can be played using ASCIIPlayback.
This is done as follows:

    $ src/asciiplaybackpygame.py FILE

where FILE is the name of the file downloaded by download\_asciimation.py.
Following our example above, this would be something like:

    $ src/asciiplaybackpygame.py 7676.json

A window should appear with the ASCIImation playing.  The player can be
controlled as described in the Controls section below.

## Controls

* **Left mouse**: restart ASCIImation
* **Esc**, **Q**: quit
* **Space**: pause/play
* **PgUp**: rewind (3 levels, x2, x4, and x8)
* **PgDn**: fast-forward (3 levels, x2, x4, and x8)

## Notes

Only the new JSON format is supported.  This shouldn't be a problem since all
ASCIImations have been converted to this new format on ASCIImator, but any old
format files need to be re-downloaded.
