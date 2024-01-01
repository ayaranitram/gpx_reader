# -*- coding: utf-8 -*-
"""
Created on Wed May 13 12:25:22 2020

@author: Martin Carlos Araya
"""

__version__ = '0.5.0'

import os
from shutil import copyfile
from stringthings import extension
from gpx_reader.calculate import md5


def rename(full_path, new_name):
    """
    renames the file on the fullPath to the newName, 
    in the same original directory

    Parameters
    ----------
    full_path : a string
        the fullpath to the file or folder to be renamed.
    new_name : a string
        the new name of the file or folder.

    Returns
    -------
    True if successfully renamed
    False if failed

    """
    if os.path.exists(extension(full_path)[3]):
        full_path = extension(full_path)[3]
    else:
        raise FileNotFoundError(full_path)
    new_name = extension(new_name)[3]
    if not os.path.isabs(new_name):
        if extension(new_name)[2] == '':
            new_name = extension(full_path)[2] + extension(new_name)[1] + extension(new_name)[0]
        else:
            raise TypeError(' newName must be a full path or simply a filename.extension')
    try:
        os.rename(full_path, new_name)
        return True
    except:
        return False


def copy(source, destination, md5_check=True):
    """
    Parameters
    ----------
    source : a string 
        the fullpath of the source file or directory to be copied.
    destination : a string 
        the fullpath of the destination,
        if destination is a directory the same filename will be used.
    md5_check : True or false
        True will check the MD5 of the copied file matches the MD5 of the source file.
        False will not check MD5.

    Returns
    -------
    True if successfully copied
         if MD5_check=True then the MD5 will be returned of successful copy
    False if failed

    """
    prepare_folder(extension(destination)[2])

    ### attempt to copy the file and calculate checksum
    if md5_check:
        md5_flag = False
        attempt = 0
        # maximum three attempts
        while attempt < 3 and md5_flag == False:
            failure = 'COPY'
            try:  # try to copy and calculate checksum
                # try to copy, message will contain the destination path 
                if failure == 'COPY':
                    message = copyfile(source, destination)
                # calculate MD5 for the original file
                try:
                    md5_str = md5(source)
                    # calculate md5 for the copied file and compare to the original's one
                    if md5_str == md5(destination):  # if OK, write to log and exit loop
                        md5_flag = True
                        failure = ''
                    else:  # if MD5s does not match, count +1 and try again
                        attempt += 1
                        md5_flag = False
                        md5_str = ''
                        failure = 'COPY'
                except:
                    failure = 'MD5'
            except:  # if try fails (mostly I/O issues during the copy or reading for the MD5)
                if failure == 'COPY':
                    attempt += 1
                elif failure == 'MD5':
                    attempt += 1
                else:
                    pass
        if md5_flag:
            return md5_str
        else:
            return False

    else:  # not MD5_check
        copy_flag = False
        attempt = 0
        # maximum three attempts
        while attempt < 3 and copy_flag == False:
            failure = 'COPY'
            try:  # try to copy
                # try to copy, message will contain the destination path 
                if failure == 'COPY':
                    message = copyfile(source, destination)
                    copy_flag = True
                    failure = ''
            except:  # if try fails (mostly I/O issues during the copy or reading for the MD5)
                if failure == 'COPY':
                    attempt += 1
                else:
                    pass

        return copy_flag


def delete(fullpath):
    """
    removes the file indicated by fullpath
    returns True if successful
    """
    try:
        os.remove(fullpath)
        return True
    except:
        return False


def move(source, destination, md5_check=True):
    """
    copy 
    if True
    delete

    Parameters
    ----------
    source : a string 
        the fullpath of the source file or directory to be copied.
    destination : a string 
        the fullpath of the destination,
        if destination is a directory the same filename will be used.

    Returns
    -------
    a tuple where:
        item 0 is the result of the copy operation:
            True or the MD5 if successful
            False if failed
        item 1 is the result of the delete operation:
            True if successful
            False if not
            None if the copy failed
    """
    cp = copy(source, destination, md5_check)
    if type(cp) is str or cp is True:
        dl = delete(source)
    else:
        dl = False
    print('MOVE', cp, dl)
    return cp, dl


__already_reported_directories__ = []


def prepare_folder(folder_path):
    """
    Create target Directory if it doesn't exist
    """
    # check if that folder already exists
    if not os.path.exists(folder_path):  # does not exist
        # level by level check that folders exists
        for i in range(5, len(folder_path.split(
                '/'))):  # starts from the 5th position on the full path because the first five items must exist: '//danas/Dig_Trans_Proj/DATALAKE_EP_PRE_INGESTION/'
            check_path = '/'.join(folder_path.split('/')[:i])
            if not os.path.exists(check_path):
                os.mkdir(check_path)
        print("Directory ", folder_path, " Created.")
        dir_msg = "Directory '" + folder_path + "' Created."
    else:  # already exists
        if folder_path not in __already_reported_directories__:
            print("Directory ", folder_path, " already exists.")
            __already_reported_directories__.append(folder_path)
        dir_msg = "Directory '" + folder_path + " already exists."
