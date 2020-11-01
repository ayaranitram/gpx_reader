#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 13:00:25 2020

@author: martin
"""

__version__ = '0.0.20-11-01'
__all__ = ['rename']


from gpx_reader.read import gpx
from gpx_reader.filehandling import listFiles , move , copy
from datafiletoolbox import extension , strDate , isDate
from os import rename
from os.path import isfile, isdir


def rename(Input,OutputFolder=None,includeOriginalFileName=True) :
    """
    Rename the 'Input' gpx file(s) according to its date, country and city,
    following the format : YYYY-##MMM-DD _ Country _ City _ original_file_name.gpx
        example:
            Input name : unglyfilename.gpx
            renamed to : 2015-05MAY-10 _ Italy _ Rome _ uglyfilename.gpx
                    
    
    Input parameter can be a folder or a gpx file. If is a folder, all the gpx
    files in that folder will be processed.
    
    If OutputFolder is not provided, the same Input folder will be assumed.
    
    To not include the original name in the the renamed file set the third parameter to False

    """
    
    if isfile(Input) :
        gpxfiles = [ Input ]
    elif isdir(Input) :
        gpxfiles = listFiles( Input , '*.gpx' )
    else :
        raise TypeError( "'Input' is not a file or a directory.")
    
    names = []
    for f in gpxfiles :
        names = extension(f)[1]
    
    Renamed = ''
    
    emptyFiles = []
    for each_file in gpxfiles :
        track = gpx(each_file)
        
        if track.start is None :
            print( '\nthe file ' + each_file + '\n  is empty' )
            newName = extension(each_file)[2] + 'empty/' + extension(each_file)[1] + extension(each_file)[0]
            move( each_file , newName )
            emptyFiles.append( newName )
        
        else :
            oldName = extension(each_file)[1]
            newName = oldName
            activity = ''
            nameDate = ''
            formatStr = ''
            for part in oldName.split() :
                if isDate(part) :
                    nameDate = part
                    formatStr = isDate(nameDate,returnFormat=True)
                if 'activity_' in part :
                    activity = part
                if nameDate != '' and activity != '' :
                    break
            if isDate(nameDate) is True and strDate(nameDate,formatIN=formatStr) == strDate(track.start) :
                newName = newName.replace(nameDate , '')
            if activity != '' :
                newName = newName.replace(activity , '')
            if track.country is not None and track.country in newName :
                newName = newName.replace(track.country , '')
            if track.city is not None and track.city in newName :
                newName = newName.replace(track.city , '')
            newName = newName.strip(' -')
            prefix = strDate( track.date , formatIN='YYYY-MM-DD',formatOUT='YYYY-MMMMM-DD' ,speak=False ) 
            if track.country is not None :
                prefix += ' _ ' + track.country
            if track.city is not None :
                prefix += ' _ ' + track.city
            elif track.county is not None :
                prefix += ' _ ' + track.county
            if len(newName) > 0 :
                newName = prefix + ' _ ' + newName
            else :
                newName = prefix
            if activity != '' :
                newName += ' _ ' + activity
    
            newPath = outputfolder + newName + '.gpx'
            nf = 0
            while isfile( newPath ) :
                nf += 1
                newPath = outputfolder + newName + '_' + str(nf) + '.gpx'
            check = copy(each_file,newPath,True)
                
            print('\nold: ' + oldName + '.gpx\nnew: ' + newName + '.gpx\nMD5: ' + check)
            Renamed += '\nold: ' + oldName + '.gpx\nnew: ' + newName + '.gpx\nMD5: ' + check