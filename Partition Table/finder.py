"""
This is duct tape code written for personal use.
It is not well tested, do not trust the results. 

Usage:
  finder <files>...
"""
VERSION="0"
from docopt import docopt
import part

def decode(file):
    f = open(file,'rb')
    i = -1
    ps_list = []
    while True:
        i = i + 1
        sector = f.read(512)
        if len(sector) < 512: break
        if sector[510:512] == '\x55\xaa':
            ps_name = 'PS'+str(i)+'.dd'
            out = open(ps_name,'wb')
            out.write(sector[446:510])
            out.close
            ps_list.append(ps_name)
            print "Found signature at",
            print i
        else:
            #print i,
            #print sector[510:512].encode('hex')
            pass
        
    for ps in ps_list:
        part.decode(ps)
        
if __name__ == '__main__':
    arguments = docopt(__doc__, version=VERSION)
    for file in arguments['<files>']:
        decode(file)
