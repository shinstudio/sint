import os, sys
from stat import *
import glob
import shutil
import tarfile
import time
import fnmatch
import install

###############################################################################
## Variables
###############################################################################
BASE_DIR  = os.path.abspath('.')
BASE_TEMP = '/tmp'
KEYWORDS  = ('meta','var','file','find','dir','command') 
###############################################################################
## Package a project based on configuration file .sicf
###############################################################################
def pkg(options):

    conf_file = find_configuration_file()
    confs = parse_configuration_file(conf_file)
    pkg_name = confs['meta']['project'] + '-' + confs['meta']['version']
    pkg_file_name = pkg_name + '-' + str(int(time.time()))

    # directories
    src_root   = BASE_DIR + '/../'
    dst_root   = BASE_TEMP + '/' + confs['meta']['project'] + '/' + confs['meta']['version']
    cur_dir    = os.getcwd()    
    build_root = BASE_DIR + '/../build'
    build_dst  = dst_root + '/sicf'

    # create temp base directory
    if not os.path.exists(dst_root):
        os.makedirs(dst_root)

    # create sicf directory and copy it to the new directory
    if not os.path.exists(build_dst):
        os.makedirs(build_dst)
    

    # create a tarfile
    tar = tarfile.open(cur_dir + '/' + pkg_file_name +  ".tar.gz", "w:gz")
    tar.dereference = False  
    # add sicf file to tar for later instruction
    for file in os.listdir(build_root):
        if fnmatch.fnmatch(file, '*.sicf'):
            shutil.copy(file, build_dst + "/" + file)
            tar.add(build_dst + "/" + file, 'sicf/' +  file)

    # jump to the temp directory to create sub directories based on sicf
    os.chdir(dst_root) 

    for dir in confs['dir']:
        if not os.path.exists(dir[4]):
            os.makedirs(dst_root + dir[4])
            tar.add(dst_root + dir[4], dir[4])

    # copy files to the temp directory by grabing files in a specified directory
    for dir in confs['find']:
        copy_tree(
            src_root + dir[4],
            dst_root + dir[5],
            False,
            options.type == 'link'
        )
        tar.add(dst_root + dir[5], dir[5])
    os.chdir(cur_dir)

    # copy individual file to the teamp directory in a specified directory
    for dir in confs['file'];
        shutil.copy2(
            src_root + dir[4],
            dst_root + dir[5]
        )
        tar.add(dst_root + dir[5], dir[5])
    os.chdir(cur_dir)
    #for file in confs['files']:
        

    # now remove temp tree
    # shutil.rmtree(BASE_TEMP + '/' + confs['meta']['project'])

    # finalize and close tar file
    tar.close()
    print "****************************************************************"
    print "Package created: " + pkg_file_name
    print "****************************************************************"
    if options.install == True:
        print ""
        print "    Installing ---> " + pkg_file_name
        print "-------------------------------------------------------------------"
        options.pkg = pkg_file_name + '.tar.gz'
        install.unpkg(options)
    else:
        print ""
        print "Install it by running: "
        print "    sominst install -p " + pkg_file_name + '.tar.gz'
        print "-------------------------------------------------------------------"


################################################################################
## Find configuration file, .sick
## It will return the first file if there are mutliple
################################################################################
def find_configuration_file():
    files = os.listdir(os.curdir)
    conf_file = ''
    for file in files:
        if file.find('.sicf') > -1:
            conf_file = file

    return conf_file

################################################################################
## parse *.sick file
## It will parse the .sick file and go through each line for a command
################################################################################
def parse_configuration_file(conf_file):
    
    SET = {}
    DIR = []
    FILE = []
    COMMAND = []
    VAR = {}
    FIND = []
    META = {}

    lines = open(conf_file, "r")
    
    for line in noblank_lines(lines):

        commandline = line.split()
        type = commandline[0]
        key = commandline[1]

        if type == 'meta':
            META[key] = get_meta(commandline)
        elif type == 'var':
            VAR[key] = get_var(commandline)
        elif type == 'set':
            SET[key] = get_set(commandline) 
        elif type == 'dir':
            DIR.append(get_dir(commandline))
        elif type == 'file':
            FILE.append(get_file(commandline))
        elif type == 'find':
            FIND.append(get_find(commandline))
    
    FIND = replace_tokenized_variables(VAR, FIND)
    META = replace_tokenized_variables(VAR, META)
    FILE = replace_tokenized_variables(VAR, FILE)
    DIR  = replace_tokenized_variables(VAR, DIR)

 
    return {'set':SET, 'var':VAR, 'meta':META, 'dir':DIR, 'file':FILE, 'command':COMMAND,'find':FIND}
################################################################################
## replace tokenized string with the internal variable
################################################################################
def replace_tokenized_variables(vars, tokens):
   
    if isinstance(tokens, dict):
        for i, j in tokens.iteritems():
            for a, b in vars.iteritems():
                tokens[i] = tokens[i].replace("$(" + a + ")", b)
        return tokens
    if isinstance(tokens, list):
        for i1 in range(len(tokens)):
            for i2 in range(len(tokens[i1])):
                for i,j in vars.iteritems():
                    tokens[i1][i2] = tokens[i1][i2].replace("$(" + i + ")", j)
        return tokens

################################################################################
## get directory value
################################################################################
def get_dir(parts):
    return parts 

def get_file(parts):
    return parts

def get_find(parts):
    return parts

################################################################################
## get set value
################################################################################
def get_set(parts):
    return ' '.join(parts[2:])
################################################################################
## get Meta data from configuration files
################################################################################
def get_meta(parts):
    return ' '.join(parts[2:])
################################################################################
## get variables from configuration files
################################################################################
def get_var(parts):
    return parts[2]

################################################################################
## go through directory tree, create symlinks, recreate the whole directory
## tree in a new location and then place those symlinks
##
## @param     src       string  source directory
## @param     recursive booelan True to include the entire subdirectories
##                              False to create specified directory with symlink
## @param     symlink   boolean True to create symlink
##                              False to copy a pysical file
################################################################################
def copy_tree(src, newdir, recursive, symlink):
    names = os.listdir(src)
    if not os.path.exists(newdir):
        os.makedirs(newdir)
    for name in names:
        if not name.startswith('.'):
            srcname = os.path.join(src, name)
            dstname = os.path.join(newdir, name)

            if os.path.isdir(srcname):
                if recursive == True:
                    copy_tree(srcname, dstname, recursive, symlink)
            else:
                # create symlink
                if os.path.isfile(dstname):
                    os.remove(dstname)
                
                if symlink == True:
                    try:
                        os.symlink(os.path.abspath(srcname), dstname)
                    except OSError:
                        print 'cannot create a symlink' 
                else:
                    try:
                        shutil.copy(srcname, dstname)
                    except OSError:
                        print 'cannot copy a file'

################################################################################
## removes blank line       
################################################################################
def noblank_lines(f):
    for l in f:
        line = l.rstrip()
        if line:
            if not line.startswith('#'):
                yield line
