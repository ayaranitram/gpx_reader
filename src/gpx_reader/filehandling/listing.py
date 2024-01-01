# -*- coding: utf-8 -*-
"""
Created on Thu May 28 11:38:00 2020

@author: Martin Carlos Araya
"""

__version__ = '0.5.20-06-05'

import fnmatch
import os

def list_files(directory, pattern=None) :
    """
    Receives a directory path, as string.
    Return a list of files in the directory and subdirectories
    
    Optional string in the 'pattern' parameter can be used to filter 
    the returned files. The matching is based on fnmatch():
            Pattern     Meaning
            *           matches everything
            ?           matches any single character
            [seq]       matches any character in seq
            [!seq]      matches any character not in seq
            
    """
    if type(directory) is str and len(directory)>1 and directory[-1] == '/' :
        directory = directory[:-1]
    list_of_files = []
    for (dirpath, dirnames, filenames) in os.walk(directory):
        for filename in filenames:
            list_of_files += [os.sep.join([dirpath, filename])]
    if pattern is None :
        return list_of_files
    elif type(pattern) is str :
        return fnmatch.filter(list_of_files,pattern)
    else :
        print('Pattern must be a string. Pattern not applied.')
        return list_of_files
    