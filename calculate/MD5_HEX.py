# -*- coding: utf-8 -*-
"""
Created on Wed May 13 11:49:22 2020

@author: MCARAYA
"""

__version__ = '0.5.20-05-13'

import hashlib

def MD5(fullPath) :
    """
    receives a path as string and evaluate MD5 using hashlib
    returns a string of the MD5 hexagesimal value of that file
    """
    md5_hash = hashlib.md5()
    File = open(fullPath, "rb")
    Content = File.read()
    md5_hash.update( Content )
    digest = md5_hash.hexdigest()
    File.close()
    return digest
