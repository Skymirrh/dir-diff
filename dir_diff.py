# -*- coding: utf-8 -*-
# Author: Skymirrh (skymirrh@skymirrh.net)
# Version: 1.0.0
"""Simple directory diff tool.

Initially developed to compare versions of ALOT (Mass Effect mod) and facilitate
upgrading by reapplying only modified textures instead of everything.

Can be used either to compare two versions of a same directory (-d) or compare
and copy differences to a separate folder (default behavior).
"""

import argparse
import os
from os.path import abspath, basename, join
import filecmp
import random
import shutil
import sys


# Override default ArgumentParser error message
class ShepardArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        print("error: {}\n".format(message))
        self.print_help()
        sys.exit(2)


# :D
def quote():
    quotes = [
        "I'm Commander Shepard, and this is my favorite store on the Citadel!",
        "I'm saving the galaxy, Shepard! I don't have time for training!",
        "Had to be me. Someone else might have gotten it wrong.",
        "Shepard.",
        "Wrex.",
        "I should go.",
        "Keelah se'lai!",
        "We'll talk later.",
        "Can it wait for a bit? I'm in the middle of some calibrations.",
        "Error: copying code is insufficient. Direct personality dissemination required.",
        "Does this unit have a soul?",
        "No tests on species with members capable of calculus. Simple rule, never broke it.",
        "Sorry babe, no sex. Just cleaned the bar."
    ]
    return random.choice(quotes)


# Command line interface
parser = ShepardArgumentParser(description="Shepard-Commander, we have devised a utility tool to compare versions of a directory and copy detected discrepancies for inspection at your private terminal!", epilog=quote(), add_help=False)
mandatory = parser.add_argument_group('Mandatory arguments')
mandatory.add_argument('prev', help="directory to compare against (usually: older version)")
mandatory.add_argument('next', help="directory to check for changes (usually: newer version)")
optional = parser.add_argument_group('Optional arguments')
optional.add_argument('changes', help="directory where to store changes", nargs='?', default='')
options = parser.add_argument_group('Options')
options.add_argument('-f', '--force', help="delete existing [changes] directory before copying", action='store_true')
options.add_argument('-d', '--diff-only', help="compare only, no copying", action='store_true')
options.add_argument('-v', '--verbose', help="display additional information", action='store_true')
options.add_argument('-h', '--help', help="show this help message and exit", action='help')
args = parser.parse_args()


# The actual magic starts here (NO CATALYST INVOLVED, I PROMISE!)
prev = abspath(args.prev)
next = abspath(args.next)
if args.verbose:
    print("""Full paths:
prev:  {}
next:  {}\n\n""".format(prev, next))

cmp = filecmp.dircmp(prev, next)
unchanged = cmp.same_files
modified = cmp.diff_files
added = cmp.right_only
removed = cmp.left_only


# Print a summary of changes
summary = """Summary of changes from {} to {}:
Unchanged: {}
Modified:  {}
Added:     {}
Removed:   {}\n\n""".format(basename(prev), basename(next), len(unchanged), len(modified), len(added), len(removed))
print(summary)


# Copying changes
if not args.diff_only:
    if args.changes != '':
        base_dir = abspath(args.changes)
    else:
        base_dir = abspath('diff-{}-to-{}'.format(basename(prev), basename(next)))
    
    if args.verbose:
        displayed_path = "\n{}".format(base_dir)
    else:
        displayed_path = basename(base_dir)
    print("Copying changes ({} files) to: {}".format(len(modified) + len(added) + len(removed), displayed_path))

    modified_dir = join(base_dir, "Modified")
    added_dir = join(base_dir, "Added")
    removed_dir = join(base_dir, "Removed")
    map = [
        (modified, modified_dir),
        (added, added_dir),
        (removed, removed_dir),
    ]
    
    # Force delete
    if args.force:
        try:
            shutil.rmtree(base_dir)
        except OSError:
            pass # If directory can't be found
    
    # Create a separate directory for each type of changes and populate
    try:
        os.makedirs(base_dir)
    except OSError:
        print("""Error: the changes directory already exists!
Delete existing directory or choose another one.
See usage help (-h) for more information.\n""")
    else:
        for list, dir in map:
            if list:
                os.makedirs(dir)
                for file in list:
                    path = join(cmp.left, file)
                    try:
                        shutil.copyfile(path, join(dir, file))
                    except IOError:
                        print("Error: can't copy file {}.".format(file))
        print("Done copying!\n\n")


# Detailed report
if args.verbose:
    details = """Details of changes from {} to {}:
==============================
Modified:
{}
==============================
Added:
{}
==============================
Removed:
{}\n""".format(basename(prev), basename(next), "\n".join(modified), "\n".join(added), "\n".join(removed))
    print(details)


# Ad astra per astera
print(quote())