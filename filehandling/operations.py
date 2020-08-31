# -*- coding: utf-8 -*-
"""
Created on Wed May 13 12:25:22 2020

@author: MCARAYA
"""

__version__ = '0.5.20-06-05'

import os
from shutil import copyfile
from datafiletoolbox import extension
from gpx_reader.calculate import MD5

def rename(fullPath,newName) :
    """
    renames the file on the fullPath to the newName, 
    in the same orginal directory

    Parameters
    ----------
    fullPath : a string 
        the fullpath to the file or folder to be renamed.
    newPathOrName : a string
        the new name of the file or folder.

    Returns
    -------
    True if succesfuly renamed
    False if failed

    """
    if os.path.exists(extension(fullPath)[3]) :
        fullPath = extension(fullPath)[3]
    else :
        raise FileNotFoundError(fullPath)
    newName = extension(newName)[3]
    if not os.path.isabs(newName) :
        if extension(newName)[2] == '' :
            newName = extension(fullPath)[2] + extension(newName)[1] + extension(newName)[0]
        else :
            raise TypeError(' newName must be a full path or simply a filename.extension')
    
    try :
        os.rename(fullPath,newName)
        return True
    except :
        return False

def copy(source,destination,MD5_check=True) :
    """
    

    Parameters
    ----------
    source : a string 
        the fullpath of the source file or directory to be copied.
    destination : a string 
        the fullpath of the destination,
        if destination is a directory the same filename will be used.
    MD5_check : True or false
        True will check the MD5 of the copied file matches the MD5 of the source file.
        False will not check MD5.

    Returns
    -------
    True if succesfuly copied
         if MD5_check=True then the MD5 will be returned of succesfull copy
    False if failed

    """
    prepareFolder( extension(destination)[2] )
    
    ### attempt to copy the file and calculate checksum
    if MD5_check :
        
        MD5_flag = False
        attempt = 0
        # maximum three attemps 
        while attempt < 3 and MD5_flag == False :
            Failure = 'COPY'
            try : # try to copy and calculate checksum
                # try to copy, message will contain the destination path 
                if Failure == 'COPY' :
                    message = copyfile(source, destination)
                # calculate MD5 for the original file
                try :
                    MD5_str = MD5(source)
                    # calculate MD5 for the copied file and compare to the original's one
                    if MD5_str == MD5(destination) : # if OK, write to log and exit loop
                        MD5_flag = True
                        Failure = ''
                    else :  # if MD5s does not match, count +1 and try again
                        attempt += 1
                        MD5_flag = False
                        MD5_str = ''
                        Failure = 'COPY'
                except :
                    Failure = 'MD5'
            except : # if try fails (mostly I/O issues during the copy or reading for the MD5)
                if Failure == 'COPY' :
                    attempt += 1
                elif Failure == 'MD5' :
                    attempt += 1
                else :
                    pass
        if MD5_flag :
            return MD5_str
        else :
            return False
                
    else : # not MD5_check 
    
        copy_flag = False
        attempt = 0
        # maximum three attemps 
        while attempt < 3 and copy_flag == False :
            Failure = 'COPY'
            try : # try to copy 
                # try to copy, message will contain the destination path 
                if Failure == 'COPY' :
                    message = copyfile(source, destination)
                    copy_flag = True
                    Failure = ''
            except : # if try fails (mostly I/O issues during the copy or reading for the MD5)
                if Failure == 'COPY' :
                    attempt += 1
                else :
                    pass
        
        return copy_flag
        

def delete(fullpath) :
    """
    removes the file indicated by fullpath
    returns True if succesful
    """
    try :
        os.remove(fullpath)
        return True
    except:
        return False

def move(source,destination,MD5_check=True) :
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
            True or the MD5 if succesful
            False if failes
        item 1 is the result of the delete operation:
            True if sucessful
            False if not
            None if the copy failed
    """
    cp = copy(source,destination,MD5_check)
    if type(cp) is str or cp is True :
        dl = delete(source)
        print('MOVE',cp,dl)
        return (cp,dl)
    else :
        print('MOVE',cp,dl)
        return (cp,None)
    
def prepareFolder(folderPath) :
    ### Create target Directory if don't exist
    # check if that folder already exists
    if not os.path.exists(folderPath): # does not exist
        # level by level check that folders exists
        for i in range(5, len(folderPath.split('/'))) : # starts from the 5th position on the full path because the first five items must exist: '//danas/Dig_Trans_Proj/DATALAKE_EP_PRE_INGESTION/'
            checkPath = '/'.join( folderPath.split('/')[:i] )
            if not os.path.exists( checkPath ) :
                os.mkdir(checkPath)
        print("Directory " , folderPath ,  " Created ")
        dirMsg = "Directory '" + folderPath + "' Created "
    else: # already exists    
        print("Directory " , folderPath ,  " already exists")
        dirMsg = "Directory '" + folderPath + " already exists"

