"""
This is duct tape code written for personal use.
It is not well tested, do not trust the results. 

Usage:
  walk <file>
"""
VERSION = "0"
from docopt import docopt
import struct

def decode(data, sector):
    offset = 0
    boot_indicator = data[offset]
    starting_chs = data[1:4]
    part_type = data[4]
    ending_chs = data[5:8]
    part_offset = data[8:12]
    part_size = data[12:16]

    #print data.encode('hex')
    if data == '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
        return False
    elif (boot_indicator != '\x80') and (boot_indicator != '\x00'):
        print 'Possible issue with sector',
        print sector
        return False
    else:
        
        #DECODE TYPE
        if part_type == '\x07':
            part_type = 'NTFS'
        elif part_type == '\x83':
            part_type = 'Ext2'
        elif part_type == '\x05':
            part_type = 'Extended Partition'
        elif part_type == '\x06':
            part_type = 'FAT16 - Over 32MB'
        elif part_type == '\x04':
            part_type = 'FAT16 - Under 32MB'
        else:
            part_type = 'UNKNOWN'
        
        #DECODE PARTITION START
        part_start = int(str(struct.unpack('<L',part_offset))[1:-2]) + sector
        
        #DECODE PARTITION END
        part_end = int(str(struct.unpack('<L',part_size))[1:-2]) + sector + part_start - 1        
        
        return [part_type,part_start,part_end]

def walk(path):
    results = []
    f = open(path,'rb')
    finished = False
    sectors = [0]
    partition_count = 0
    print 'MBR/EPB\tPartition#\tPartition Type\tStart Sector\tEnd Sector'
    while sectors:
        sector = sectors.pop()
        f.seek((sector*512)+446)
        partition_table = f.read(64)
        for entry in range(4):
            decoded_enrty = decode(partition_table[entry*16:entry*16+16],sector)
            if decoded_enrty:
                if decoded_enrty[0] == 'Extended Partition':
                    sectors.append(decoded_enrty[1])
                
                print sector,
                print '\t',
                if decoded_enrty[0] != 'Extended Partition':
                    partition_count = partition_count + 1
                    print partition_count,
                print '\t',
                print decoded_enrty[0],
                print '\t',
                print decoded_enrty[1],
                print '\t',
                print decoded_enrty[2]

if __name__ == '__main__':
    arguments = docopt(__doc__, version=VERSION)
    walk(arguments['<file>'])