#! /usr/bin/env python

import os, sys
import shutil
from optparse import OptionParser


CUR_DIR = os.getcwd()

################################################################################
## main method
################################################################################
def main():

    parser = OptionParser()
    parser.add_option("-l", "--symlink", help='symlink instead of hard installation')

    (options, args) = parser.parse_args()

    install(options)

################################################################################
## install method
################################################################################
def install(options):

    DEST_LIB_DIR = "/usr/lib/sominst"
    DEST_BIN_DIR = "/usr/bin"

    SOMINST_SYMLINK = os.path.join(DEST_BIN_DIR, "sominst")
    SOMINST_LIB_DIR = os.path.join(DEST_LIB_DIR, "sominst")
    SOMINST_FILE = os.path.join(DEST_LIB_DIR, "sominst.py")

    BASE_DIR  = os.getcwd() 
    
    # create temp base directory
    if not os.path.exists(DEST_LIB_DIR):
        print "############################################################"
        print "## Destination directory does not exist"
        print "##   creating ... "
        print DEST_LIB_DIR
        os.makedirs(DEST_LIB_DIR)

    # directory exist already, so clean files first
    if os.path.exists(DEST_LIB_DIR):
        print "############################################################"
        print "## Cleaning old files"
        for the_file in os.listdir(DEST_LIB_DIR):
            file_path = os.path.join(DEST_LIB_DIR, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception, e:
                print e

    # check sominst symlink in /usr/bin if exists, remove it
    try:
        if os.path.exists(SOMINST_SYMLINK):
            print "###########################################################"
            print "## Removing old file /usr/bin/symlink"
            os.unlink(SOMINST_SYMLINK)
    except IOError:
        pass
    #if os.path.exists(SOMINST_SYMLINK):
    #    print "removing symlink: ", SOMINST_SYMLINK
    #    os.unlink(os.path.join(DEST_BIN_DIR,"sominst"))

    # copy
    shutil.copytree(os.path.join(BASE_DIR, "sominst"), SOMINST_LIB_DIR)
    shutil.copy2(os.path.join(BASE_DIR, "sominst.py"), SOMINST_FILE)
    os.symlink(SOMINST_FILE, SOMINST_SYMLINK)

    print "####################################################################"
    print "### sominst was successfully installed"
    print "####################################################################"
################################################################################
## execute the program
################################################################################
if __name__ == '__main__':
    sys.exit(main())
