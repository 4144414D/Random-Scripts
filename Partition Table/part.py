"""
This is duct tape code written for personal use.
It is not well tested, do not trust the results. 

Usage:
  part <files>...
"""
VERSION="0"
from docopt import docopt
import struct

def chs(bytes):
    binary = lambda x: " ".join(reversed( [i+j for i,j in zip( *[ ["{0:04b}".format(int(c,16)) for c in reversed("0"+x)][n::2] for n in [1,0] ] ) ] ))
    sector = str(int('00' + binary(bytes[1].encode('hex'))[2:], 2))
    head = str(struct.unpack('<b',bytes[0]))[1:-2]
    cylinder_low_byte = binary(bytes[2].encode('hex'))
    cylinder_high_bits = binary(bytes[1].encode('hex'))[:2]
    cylinder = str(int(cylinder_high_bits + cylinder_low_byte, 2))
    return '(' + cylinder + '/' + head + '/' + sector + ')'

def decode(file):
    #print file
    C = 98988 #count from 1
    H = 2 #count from 0
    S = 32 #count from 1
    
    data = open(file,'rb').read(64)
    i = 0
    good = True
    for i in range(4):
        if (data[i*16] != '\x00') and (data[i*16] != '\x80'):
            good = False
    if data == '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
        good = False
    if good:
        print file
        for entry in range(4):
            print 'Partition Entry ' + str(entry + 1) + ':'
            offset = (entry) * 16
            
            full_entry =  data[offset:offset+16]
            boot_indicator = data[offset]
            starting_chs = data[offset+1:offset+4]
            part_type = data[offset+4]
            ending_chs = data[offset+5:offset+8]
            part_offset = data[offset+8:offset+12]
            part_size = data[offset+12:offset+16]
            
            
            
            
            if full_entry == '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
                print full_entry.encode('hex')
                print 'Empty entry'
            elif (boot_indicator != '\x80') and (boot_indicator != '\x00'):
                print "Likely false partition detected"
            else:
                #Active Partition
                print full_entry.encode('hex')
                print boot_indicator.encode('hex'),
                if boot_indicator == '\x80':
                    print '= Active Partition'
                elif boot_indicator == '\x00':
                    print '= Not Active Partition'
                else:
                    print '= Likely false partition detected'
                
                #Starting CHS
                print ' ',
                print starting_chs.encode('hex'),
                print '= Starting C/H/S',
                print chs(starting_chs)
            
                #Partition Type
                print '       ',
                print part_type.encode('hex'),
                print '= Partition Type',
                if part_type == '\x07':
                    print '(NTFS)'
                elif part_type == '\x83':
                    print '(Ext2)'
                elif part_type == '\x05':
                    print '(Extended Partition)'
                elif part_type == '\x06':
                    print '(FAT16 - Over 32MB)'
                elif part_type == '\x04':
                    print '(FAT16 - Under 32MB)'
                else:
                    print '(UNKNOWN)'
                    
                    
                #Ending CHS
                print '         ',
                print ending_chs.encode('hex'),
                print '= Ending C/H/S',
                print chs(ending_chs)
                
                #Partition Offset
                print '               ',
                print part_offset.encode('hex'),
                print '= Partition Offset',
                print str(struct.unpack('<L',part_offset))[:-2] + ')'
                
                #Partition Size
                print '                       ',
                print part_size.encode('hex'),
                print '= Partition Size',
                print str(struct.unpack('<L',part_size))[:-2] + ')'
            print
    
    
if __name__ == '__main__':
    arguments = docopt(__doc__, version=VERSION)
    for file in arguments['<files>']:
        decode(file)
