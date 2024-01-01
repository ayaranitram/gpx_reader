#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 14:34:40 2020

@author: Martin Carlos Araya
"""

from gpx_reader.read import gpx
from gpx_reader.filehandling import list_files, move, copy
from stringthings import extension, date, is_date
from os.path import isfile


input_folder = '//home/Mis Fotos/_MyTracks/gpx/'  # '/Volumes/Mis Fotos/_MyTracks/gpx_unsorted'
# input_folder = '/Volumes/Mis Fotos/_MyTracks/kml2gpx/'
output_folder = '//home/Mis Fotos/_MyTracks/gpx_sorted/'  # '/Volumes/Mis Fotos/_MyTracks/gpx_sorted/'
# output_folder = '/Volumes/Mis Fotos/_MyTracks/kml2gpx/renamed/'

gpx_files = list_files(input_folder, '*.gpx')


Renamed = ''

empty_files = []
for each_file in gpx_files :
    track = gpx(each_file)
    
    if track.start is None :
        print( '\nthe file ' + each_file + '\n  is empty' )
        new_name = extension(each_file)[2] + 'empty/' + extension(each_file)[1] + extension(each_file)[0]
        move(each_file, new_name)
        empty_files.append(new_name)
    
    else :
        old_name = extension(each_file)[1]
        new_name = old_name
        activity = ''
        name_date = ''
        format_str = ''
        for part in old_name.split() :
            if is_date(part) :
                name_date = part
                format_str = is_date(name_date, return_format=True)
            if 'activity_' in part :
                activity = part
            if name_date != '' and activity != '' :
                break
        if is_date(name_date) is True and date(name_date, format_in=format_str) == date(track.start):
            new_name = new_name.replace(name_date, '')
        if activity != '' :
            new_name = new_name.replace(activity, '')
        if track.country is not None and track.country in new_name :
            new_name = new_name.replace(track.country, '')
        if track.city is not None and track.city in new_name :
            new_name = new_name.replace(track.city, '')
        new_name = new_name.strip(' -')
        prefix = date( track.date , format_in='YYYY-MM-DD', format_out='YYYY-MMMMM-DD', verbose=False)
        if track.country is not None :
            prefix += ' _ ' + track.country
        if track.city is not None :
            prefix += ' _ ' + track.city
        elif track.county is not None :
            prefix += ' _ ' + track.county
        if len(new_name) > 0 :
            new_name = prefix + ' _ ' + new_name
        else :
            new_name = prefix
        if activity != '' :
            new_name += ' _ ' + activity

        newPath = output_folder + new_name + '.gpx'
        nf = 0
        while isfile( newPath ) :
            nf += 1
            newPath = output_folder + new_name + '_' + str(nf) + '.gpx'
        check = copy(each_file,newPath,True)
            
        print('\nold: ' + old_name + '.gpx\nnew: ' + new_name + '.gpx\nMD5: ' + check)
        Renamed += '\nold: ' + old_name + '.gpx\nnew: ' + new_name + '.gpx\nMD5: ' + check