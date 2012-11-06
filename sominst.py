#! /usr/bin/env python26
# Usage
# {command} : install, create, remove
# {symlink} : link
#
# sudo ./sominst {command} --type={type}


import os
import sys
from optparse import OptionParser
from sominst import create
from sominst import install

BASE = os.pardir # base directory

################################################################################
## main method
################################################################################
def main():
    
    parser = OptionParser()
    parser.add_option("-t", "--type", help='type of package when creating')
    parser.add_option("-p", "--pkg", help='package file name')
    
    (options, args) = parser.parse_args()

    if len(args) > 0:

        COMMAND = args[0]

        if COMMAND == 'install':
            install.unpkg(options) 

        if COMMAND == 'create':
            create.pkg(options)

        if COMMAND == 'set':
            print 'set'

        if COMMAND == 'unset':
            print 'unset'

        if COMMAND == 'delete':
            print 'delete'

    
    #conf_file = find_configuration_file()
    
    #if not conf_file == '':
    #    parse_configuration_file(conf_file)
    #else:
    #    print "There is no .sick file to process."
    return 0

################################################################################
## execute the program
################################################################################
if __name__ == '__main__':
    sys.exit(main())
