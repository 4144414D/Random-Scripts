"""
This is duct tape code written for personal use.
It is not well tested, do not trust the results. 

This should reduce a text file to it's unique lines,
and store them in length order in a new file. 

Usage:
   unique <files>...
"""
VERSION="0"
from docopt import docopt
import struct

def unique(file):
    f = open(file)
    unique_set = set([])
    for line in f: unique_set.add(line)
    f.close()
    file = file + '_unique.txt'
    list = []
    for item in unique_set: list.append(item)
    list.sort(key=len)
    f = open(file,'w')
    for item in list: f.write(item)
    f.close

if __name__ == '__main__':
    arguments = docopt(__doc__, version=VERSION)
    for file in arguments['<files>']: unique(file)