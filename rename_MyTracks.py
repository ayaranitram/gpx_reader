#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 14:34:40 2020

@author: martin
"""

from gpx_reader.read import gpx
from gpx_reader.filehandling import listFiles , move 
from datafiletoolbox import extension , date
from datafiletoolbox.common.stringformat import isDate
from os import rename, isfile

gpxfiles = listFiles( '/Volumes/Mis Fotos/_MyTracks/gpx' , '*.gpx' )

names = []
for f in gpxfiles :
    names = extension(f)[1]

loaded = gpx(gpxfiles[78])

testingRename = ''

emptyFiles = []
for each_file in gpxfiles[:10] + gpxfiles[50:70] + gpxfiles[-10:] :
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
        if isDate(nameDate) is True and date(nameDate,formatIN=formatStr) == date(track.start) :
            newName = newName.replace(nameDate , '')
        if activity != '' :
            newName = newName.replace(activity , '')
        if track.country is not None and track.country in newName :
            newName = newName.replace(track.country , '')
        if track.city is not None and track.city in newName :
            newName = newName.replace(track.city , '')
        newName = newName.strip(' -')
        prefix = date( track.date , formatIN='YYYY-MM-DD',formatOUT='YYYY-MMMMM-DD' ,speak=False ) 
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

        if newName in names :
            
        print('\nold: ' + oldName + '\nnew: ' + newName )
        testingRename += '\nold: ' + oldName + '\nnew: ' + newName 


