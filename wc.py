"""
NAME
       wc - print newline, word, and byte counts for each file

SYNOPSIS
       wc [OPTION]... [FILE]...
       wc [OPTION]... --files0-from=F

DESCRIPTION
       Print  newline,  word,  and  byte  counts  for  each  FILE,  and  a  total  line  if more than one FILE is specified.  A word is a
       non-zero-length sequence of characters delimited by white space.

       With no FILE, or when FILE is -, read standard input.

       The options below may be used to select which counts are printed, always in the following order: newline, word,  character,  byte,
       maximum line length.

       -c, --bytes
              print the byte counts

       -m, --chars
              print the character counts

       -l, --lines
              print the newline counts

       --files0-from=F
              read input from the files specified by NUL-terminated names in file F; If F is - then read names from standard input

       -L, --max-line-length
              print the maximum display width

       -w, --words
              print the word counts

       --help display this help and exit

       --version
              output version information and exit
"""

import io
import logging
import sys
import os
import traceback
import argparse
import re

logger = None

def main():
    parser = argparse.ArgumentParser(description="print newline, word, and byte counts for each file",
            formatter_class=argparse.RawDescriptionHelpFormatter, epilog="")
    parser.add_argument('-c', '--bytes', action='store_true', help='print the byte counts')
    parser.add_argument('-m', '--chars', action='store_true', help='print the character counts')
    parser.add_argument('-l', '--lines', action='store_true', help='print the newline counts')
    parser.add_argument('-w', '--words', action='store_true', help='print the word counts')
    parser.add_argument('--version', action='store_true', help='output version information and exit')
    parser.add_argument('FILE', action='store', nargs="*", help="Input file")
    args = parser.parse_args()

    for FILE in args.FILE:
        try:
            with open(FILE, "rb") as fp:
                lines = 0
                bites = 0
                chars = 0
                words = 0
                for line in fp.readlines():
                    lines = lines + 1
                    bites = bites + len(line)
                    chars = chars + len(line.decode())
                    words = words + len([w for w in re.split(r'\s+', line.decode()) if 0 < len(w)])
            output = ""
            if args.lines:
                output = "{1} {0}".format(lines, output)
            if args.words:
                output = "{1} {0}".format(words, output)
            if args.bytes:
                output = "{1} {0}".format(bites, output)
            if args.chars:
                output = "{1} {0}".format(chars, output)
            logger.info("{0} {1}".format(output, FILE))
        except Exception as e:
            logger.error("Could not access file {0}".format(FILE))
    if args.version:
        logger.info("{0} 0.1".format(sys.argv[0]))
        exit(0)
    exit(0)

if __name__ == "__main__":
    try:
        logFormatter = logging.Formatter("%(asctime)s [%(levelname)-8.8s %(filename)s:%(lineno)4d]  %(message)s")
        logger = logging.getLogger()
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        logger.addHandler(consoleHandler)
        logger.setLevel(logging.INFO)
        logger.info('Command line: {0}'.format(' '.join(sys.argv)))
        main()
    except Exception as e:
        fp = io.StringIO()
        logger.critical('Unhandled exception: {0}'.format(type(e)))
        logger.critical('Arguments: {0}'.format(e.args))
        traceback.print_exc(file=fp)
        for line in fp.getvalue().splitlines():
            logger.critical(line.strip())
        exit(-1)

