#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 14:34:40 2020

@author: martin
"""

from gpx_reader.read import gpx
from gpx_reader.filehandling import listFiles , move , copy
from datafiletoolbox import extension , strDate , isDate
from os import rename
from os.path import isfile


inputfolder = '/Volumes/Mis Fotos/_MyTracks/gpx_unsorted'
# inputfolder = '/Volumes/Mis Fotos/_MyTracks/kml2gpx/'
outputfolder = '/Volumes/Mis Fotos/_MyTracks/gpx_sorted/' 
# outputfolder = '/Volumes/Mis Fotos/_MyTracks/kml2gpx/renamed/'

gpxfiles = listFiles( inputfolder , '*.gpx' )

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


