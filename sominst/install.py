# import global modules
import os, sys
import shutil
import tarfile
import time

# import create module in sominst
import create

###############################################################################
## global variable within this module
###############################################################################
CUR_DIR = os.getcwd()

###############################################################################
## install a pkg
###############################################################################
def unpkg(options):
    
    if str(options.pkg) == 'None':
        pkg_file = find_package_file()
    else:
        pkg_file = options.pkg

    project_list = parse_pkg_name(pkg_file)

    tmp_root = '/var/lib/sominst/' + project_list[0] + '/' + project_list[1]
        
    if len(project_list) == 3:
        tmp_root = tmp_root + '-' + project_list[2].replace('.tar.gz','')

    if pkg_file is False:
        print 'Package file not found. Did you create a package file?'
    else:
        if not os.path.exists(tmp_root):
            os.makedirs(tmp_root)
        
        uncompress(tmp_root, pkg_file)
        os.chdir(tmp_root + '/sicf')
        sicf_file = create.find_configuration_file()
        # now get the parsed sicf info
        confs = create.parse_configuration_file(sicf_file)
        os.chdir(CUR_DIR)

        # now let's create directories if not exists
        for dir in confs['dir']:
            if not os.path.exists(dir[4]):
                os.makedirs(dir[4])
                print 'creating a directory ---> ' + dir[4]
            else:
                print 'a directory exists already ---> ' + dir[4]

        # first let's remove all files that belong to this project
        for dir in confs['find']:
            files = os.listdir(tmp_root + dir[5])
            for file in files:
                if os.path.isfile('/'+dir[5]+'/'+file):
                    os.remove('/'+dir[5]+'/'+file)

        # now copy files to the destination directory
        for dir in confs['find']:
            files = os.listdir(tmp_root + dir[5])
            for file in files:
                dst_filepath = dir[5] + '/' + file
                src_filepath = tmp_root + '/' + dir[5] + '/' + file
                print 'copying a file ---> ' + dst_filepath 
                if os.path.islink(src_filepath):
                    linkname = os.readlink(src_filepath)
                    os.symlink(linkname, dst_filepath)
                if not os.path.islink(src_filepath):
                    if not os.path.isdir(src_filepath):
                        shutil.copy(src_filepath, dst_filepath)

def find_package_file():
    names = os.listdir(CUR_DIR)
    for name in names:
        if 'tar.gz' in name:
            return name
    return False

def parse_pkg_name(file):
    tokens = file.split('-')
    return tokens

def uncompress(tmp_root, file):

    try:
        tar = tarfile.open(file, "r:gz")
        
        for tarinfo in tar:
            if tarinfo.isreg():
                tar.extract(tarinfo, tmp_root)
            if tarinfo.isdir():
                tar.extract(tarinfo, tmp_root)
            if tarinfo.issym():
                tar.extract(tarinfo, tmp_root)
                if os.path.isfile(tmp_root + '/' + tarinfo.name):
                    os.remove(tmp_root + '/' + tarinfo.name)
                os.symlink(tarinfo.linkname, tmp_root + '/' + tarinfo.name)
    except:
        print "Could not open " + file

# def deploy(sicf):
    



