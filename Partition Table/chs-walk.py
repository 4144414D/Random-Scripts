"""
This is duct tape code written for personal use.
It is not well tested, do not trust the results. 

Usage:
  walk <file>
"""
VERSION = "0"
from docopt import docopt
import struct

def chs_decode(bytes):
    binary = lambda x: " ".join(reversed( [i+j for i,j in zip( *[ ["{0:04b}".format(int(c,16)) for c in reversed("0"+x)][n::2] for n in [1,0] ] ) ] ))
    sector = str(int('00' + binary(bytes[1].encode('hex'))[2:], 2))
    head = str(struct.unpack('<b',bytes[0]))[1:-2]
    cylinder_low_byte = binary(bytes[2].encode('hex'))
    cylinder_high_bits = binary(bytes[1].encode('hex'))[:2]
    cylinder = str(int(cylinder_high_bits + cylinder_low_byte, 2))
    return [int(cylinder), int(head), int(sector)]
    
def decode(data, sector, heads, sectors):
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
        
        #DECODE LBA PARTITION START
        part_start = int(str(struct.unpack('<L',part_offset)).replace('L','')[1:-2]) + sector
        
        #DECODE CHS PARTITION START
        chs = chs_decode(starting_chs)
        chs_start_val = '('+str(chs[0])+'/'+str(chs[1])+'/'+str(chs[2])+')'
        chs_start = ((chs[0] * heads * sectors) + (chs[1] * sectors) + (chs[2] - 1))
        
        #DECODE LBA PARTITION END
        part_size = int(str(struct.unpack('<L',part_size)).replace('L','')[1:-2])
        part_end = part_size + (part_start - 1)   

        #DECODE CHS PARTITION END
        chs = chs_decode(ending_chs)
        chs_end_val = '('+str(chs[0])+'/'+str(chs[1])+'/'+str(chs[2])+')'
        chs_end = ((chs[0] * heads * sectors) + (chs[1] * sectors) + (chs[2] - 1))
        
        return [part_type,part_start,part_end,chs_start,chs_end,chs_start_val,chs_end_val]

def walk(path, heads, sectors_count):
    results = []
    f = open(path,'rb')
    finished = False
    sectors = [0]
    partition_count = 0
    print 'MBR/EPT\tPartition#\tPartition Type\tLBA Start Sector\tLBA End Sector\tCHS Start (Converted)\tCHS End (Converted)\tCHS Start\tCHS End'
    while sectors:
        sector = sectors.pop()
        f.seek((sector*512)+446)
        partition_table = f.read(64)
        for entry in range(4):
            decoded_enrty = decode(partition_table[entry*16:entry*16+16],sector,heads,sectors_count)
            if decoded_enrty:
                if decoded_enrty[0] == 'Extended Partition':
                    sectors.append(decoded_enrty[3])
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
                print decoded_enrty[2],
                print '\t',
                print decoded_enrty[3],
                print '\t',
                print decoded_enrty[4],
                print '\t',
                print decoded_enrty[5],
                print '\t',
                print decoded_enrty[6]

if __name__ == '__main__':
    arguments = docopt(__doc__, version=VERSION)
    walk(arguments['<file>'], 128, 63)