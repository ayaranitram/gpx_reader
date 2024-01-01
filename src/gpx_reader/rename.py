#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 13:00:25 2020

@author: Martin Carlos Araya
"""

__version__ = '0.0.20-11-01'
__all__ = ['rename']


from .read import GPX
from .filehandling import list_files , move , copy
from stringthings import extension, date, is_date
from os.path import isfile, isdir, dirname


def rename(input_files, output_folder=None, include_original_file_name=True) :
    """
    Rename the 'input_files' gpx file(s) according to its date, country and city,
    following the format : YYYY-##MMM-DD _ Country _ City _ original_file_name.gpx
        example:
            Input name : ugly-filename.gpx
            renamed to : 2015-05MAY-10 _ Italy _ Rome _ ugly-filename.gpx
                    
    
    Input parameter can be a folder or a gpx file. If is a folder, all the gpx
    files in that folder will be processed.
    
    If OutputFolder is not provided, the same Input folder will be assumed.
    
    To not include the original name in the renamed file set the third parameter to False.
    """
    if type(input_files) is list:
        for each in input_files:
            rename(each, output_folder=output_folder, include_original_file_name=include_original_file_name)

    if isfile(input_files):
        gpx_files = [input_files]
    elif isdir(input_files):
        gpx_files = list_files(input_files, '*.gpx')
    else :
        raise TypeError( "'Input' is not a file or a directory.")
    
    if output_folder is not None:
        if isdir(output_folder):
            output_folder = output_folder
    else :
        if isdir(input_files):
            output_folder = input_files
        elif isfile(input_files):
            output_folder = dirname(input_files)
    
    renamed = ''
    
    empty_files = []
    for each_file in gpx_files :
        track = GPX(each_file)
        
        if track.start is None :
            print(f'\nthe file {each_file} \n  is empty')
            new_name = extension(each_file)[2] + 'empty/' + extension(each_file)[1] + extension(each_file)[0]
            move(each_file, new_name)
            empty_files.append(new_name)
        
        else :
            old_name = extension(each_file)[1] if include_original_file_name else ''
            new_name = old_name
            activity = ''
            name_date = ''
            format_str = ''
            for part in old_name.split() :
                if is_date(part) :
                    name_date = part
                    format_str = is_date(name_date,return_format=True)
                if 'activity_' in part :
                    activity = part
                if name_date != '' and activity != '' :
                    break
            if is_date(name_date) is True and date(name_date,format_in=format_str) == date(track.start) :
                new_name = new_name.replace(name_date , '')
            if activity != '' :
                new_name = new_name.replace(activity , '')
            if track.country is not None and track.country in new_name :
                new_name = new_name.replace(track.country , '')
            if track.city is not None and track.city in new_name :
                new_name = new_name.replace(track.city , '')
            new_name = new_name.strip(' -')
            prefix = date( track.date , format_in='YYYY-MM-DD',format_out='YYYY-MMMMM-DD' ,verbose=False )
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
    
            new_path = output_folder + new_name + '.gpx'
            nf = 0
            while isfile( new_path ) :
                nf += 1
                new_path = output_folder + new_name + '_' + str(nf) + '.gpx'
            check = copy(each_file,new_path,True)
                
            print('\nold: ' + old_name + '.gpx\nnew: ' + new_name + '.gpx\nMD5: ' + check)
            renamed += '\nold: ' + old_name + '.gpx\nnew: ' + new_name + '.gpx\nMD5: ' + check
