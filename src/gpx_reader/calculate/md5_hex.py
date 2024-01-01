# -*- coding: utf-8 -*-
"""
Created on Wed May 13 11:49:22 2020

@author: Martin Carlos Araya
"""

__version__ = '0.5.0'

import hashlib

def md5(fullPath) :
    """
    receives a path as string and evaluate MD5 using hashlib
    returns a string of the MD5 hexadecimal value of that file
    """
    md5_hash = hashlib.md5()
    file = open(fullPath, "rb")
    content = file.read()
    md5_hash.update(content)
    digest = md5_hash.hexdigest()
    file.close()
    return digest
