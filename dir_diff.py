# -*- coding: utf-8 -*-
# Author: Skymirrh (skymirrh@skymirrh.net)
# Version: 1.1.0
"""Simple directory diff tool.

Initially developed to compare versions of ALOT (Mass Effect mod) and facilitate
upgrading by reapplying only modified textures instead of everything.

Can be used either to compare two versions of a same directory (-d) or compare
and copy differences to a separate folder (default behavior).
"""

import argparse
import os
from os.path import abspath, basename, isdir, join, relpath
import filecmp
import random
import shutil
import sys


class DirDiff(object):
    """Main class, basically a wrapper around filecmp.dircmp with syntactic sugar."""
    def __init__(self, prev_dir, next_dir, changes_dir=''):
        # Directories
        self.prev_dir = abspath(prev_dir)
        self.next_dir = abspath(next_dir)
        if changes_dir != '':
            self.changes_dir = abspath(changes_dir)
        else:
            self.changes_dir = abspath('diff-{}-to-{}'.format(basename(self.prev_dir), basename(self.next_dir)))

        # Initializing diff lists
        self.unchanged = []
        self.modified = []
        self.added = []
        self.removed = []

        # Compare
        dircmp = filecmp.dircmp(prev_dir, next_dir)
        self.analyze(dircmp)

    def analyze(self, dircmp):
        # Analyze dircmp output and sort into lists, then recursively analyze common subdirectories.
        self.unchanged += dircmp.same_files
        self.modified += [relpath(join(dircmp.right, diff_file), self.next_dir) for diff_file in dircmp.diff_files]
        self.added += [relpath(join(dircmp.right, new_file), self.next_dir) for new_file in dircmp.right_only]
        self.removed += [relpath(join(dircmp.left, del_file), self.prev_dir) for del_file in dircmp.left_only]
        for subdir in dircmp.subdirs.itervalues():
            self.analyze(subdir)

    def print_summary(self):
        """Print a summary of changes."""
        summary = """Summary of changes from {} to {}:
Unchanged: {}
Modified:  {}
Added:     {}
Removed:   {}\n\n""".format(basename(self.prev_dir), basename(self.next_dir),
                            len(self.unchanged), len(self.modified), len(self.added), len(self.removed))
        print(summary)

    def print_details(self):
        """Print a detailed report of changes."""
        details = """Details of changes from {} to {}:
==============================
Modified:
{}
==============================
Added:
{}
==============================
Removed:
{}\n\n""".format(basename(self.prev_dir), basename(self.next_dir),
                 "\n".join(self.modified), "\n".join(self.added), "\n".join(self.removed))
        print(details)

    def print_paths(self):
        """Print full paths of directories."""
        print("""Full paths:
prev:    {}
next:    {}
changes: {}\n\n""".format(self.prev_dir, self.next_dir, self.changes_dir))

    def copy_changes(self, force_delete=False):
        """Copy detected changes to a new folder for easy inspection."""
        # Delete changes directory if --force-delete specified
        if force_delete:
            try:
                print("Deleting changes directory.")
                shutil.rmtree(self.changes_dir)
            except OSError:
                pass  # If directory can't be found

        print("Copying changes ({} files) to {}".format(len(self.modified) + len(self.added) + len(self.removed),
                                                        basename(self.changes_dir)))
        modified_dir = join(self.changes_dir, "Modified")
        added_dir = join(self.changes_dir, "Added")
        removed_dir = join(self.changes_dir, "Removed")
        dir_map = [  # (changes paths, destination directory, original directory)
            (self.modified, modified_dir, self.next_dir),
            (self.added, added_dir, self.next_dir),
            (self.removed, removed_dir, self.prev_dir),
        ]

        # Try to create changes directory
        try:
            os.makedirs(self.changes_dir)
        except OSError:
            print("""Error: the changes directory already exists!
Delete existing directory (-f) or choose another one ([changes]).
See usage help (-h) for more information.\n""")
        else:  # We're good, create a separate directory for each type of changes and populate
            for changes, destination_directory, original_directory in dir_map:
                if changes:
                    os.makedirs(destination_directory)
                    for change in changes:
                        path = join(original_directory, change)
                        try:
                            if isdir(path):
                                shutil.copytree(path, join(destination_directory, change))
                            else:
                                shutil.copyfile(path, join(destination_directory, change))
                        except IOError:
                            print("Error: can't copy file {}.".format(change))
            print("Done copying!\n\n")


class ShepardArgumentParser(argparse.ArgumentParser):
    def __init__(self):
        super(ShepardArgumentParser, self).__init__(description="Shepard-Commander, we have devised a utility tool to \
        compare versions of a directory and copy detected discrepancies for inspection at your private terminal!",
                                                    epilog=quote(), add_help=False)

        mandatory = self.add_argument_group('Mandatory arguments')
        mandatory.add_argument('prev', help="directory to compare against (usually: older version)")
        mandatory.add_argument('next', help="directory to check for changes (usually: newer version)")

        optional = self.add_argument_group('Optional arguments')
        optional.add_argument('changes', help="directory where to store changes", nargs='?', default='')

        options = self.add_argument_group('Options')
        options.add_argument('-f', '--force-delete', help="delete existing [changes] directory before copying",
                             action='store_true')
        options.add_argument('-d', '--diff-only', help="compare only, no copying", action='store_true')
        options.add_argument('-v', '--verbose', help="display additional information", action='store_true')
        options.add_argument('-h', '--help', help="show this help message and exit", action='help')

    def error(self, message):
        # Override default error message to print help when user supplies invalid arguments
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
        "Sorry babe, no sex. Just cleaned the bar.",
        "I’m sorry, I’m having trouble hearing you. I’m getting a lot of bullshit on this line.",
        "That doesn’t explain why you used my armor to fix yourself. - ...There was a hole.",
        "I enjoy the sight of humans on their knees.",
        "I've had enough of your tabloid journalism.",
        "That was for Thane, you son of a bitch!",
        "I'm Garrus Vakarian, and this is my favorite spot on the Citadel!",
        "This is just a fling, Vakarian. I'm using you for your body.",
        "You're so mean... and I'm okay with that.",
        "If this thing goes sideways and we end up on the other side, meet me at the bar. I'm buying.",
        "Emergency Induction Port!",
        "They tell me it's a suicide mission. I intend to prove them wrong.",
        "Hell yeah... put more of the stuff in the... the thing where stuff goes in.",
        "Conrad, let me make this perfectly clear. *thump* This is not acceptable.",
        "The universe is a dark place. I'm trying to make it brighter before I die.",
        "...So, fuck you. And thanks for asking.",
        "I had reach, but she had flexibility.",
        "I am the very model of a scientist salarian!",
        "I am pure Krogan. You should be in awe.",
        "Windows are structural weaknesses, Geth do not use them.",
        "ASSUMING DIRECT CONTROL!",
        "Don't fuck with Aria.",
        "Stand in the ashes of a trillion dead souls, and ask if honor matters. The silence is your answer.",
        "I am a biotic god! I think things, and they happen! Fear me, lesser creatures, for I am biotics made flesh!",
    ]
    return random.choice(quotes)


# Command line interface
parser = ShepardArgumentParser()
args = parser.parse_args()

# The actual magic starts here (NO CATALYST INVOLVED, I PROMISE!)
dir_diff = DirDiff(args.prev, args.next, args.changes)

# Print full paths only in --verbose mode
if args.verbose:
    dir_diff.print_paths()

# Always print summary
dir_diff.print_summary()

# Always copy, unless --diff-only is specified
if not args.diff_only:
    dir_diff.copy_changes(force_delete=args.force_delete)

# Print details only in --verbose mode
if args.verbose:
    dir_diff.print_details()

# Ad astra per astera
print(quote())
