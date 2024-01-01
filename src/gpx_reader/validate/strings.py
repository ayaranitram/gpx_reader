# -*- coding: utf-8 -*-
"""
Created on Wed May 13 10:42:52 2020

@author: MCARAYA
"""

__version__ = '0.5.20-06-05'

import datetime

class UndefinedDateFormat(Exception) :
    pass

def valid_characters(string, returnString=False) :
    """
    Validates a string to be compliant with DL structure
    
    Parameters
    ----------
    string : the string to be validated
    returnString : True returns the compliant string,
                   False returns True or False according to the input string  
    
    
    Returns
    -------
    True if String is compliant
    False if not compliant
    
    if returnString=True then modified String will be returned.
    """
    # remove blank spaces and beginning and end and make UPPERCASE
    new_string = string.upper().strip()
    # replace special characters by '_'
    for s in [',','(',')','=','+','#','.',';',' '] :
        new_string = new_string.replace(s,'_')
    # replace '&' by '_AND_'
    new_string = new_string.replace('&','_AND_')
    
    # eliminate double '_'
    while '__' in new_string :
        new_string = new_string.replace('__','_')
    
    # remove '_' and the begging and end of the file name, then concatenate the extension in uppercase
    new_string = new_string.strip('_')
    
    if not returnString :
        return new_string == string
    else : # returnString == True
        return new_string


def isDate(stringDate, returnString=False) :
    CurrentYear = int(str(datetime.datetime.now())[:4])
    NewString = ''
    
    # if the string is not digit, might be a date formated 'DD-MMM-YYYY'
    if not stringDate.isdigit() :
        try:
            NewString = strDate( stringDate , formatOUT='YYYYMMDD')
        except :
            NewString = ''
        if returnString :
            return NewString
        else :
            return False 
    
    # check YYYYMMDD
    if len(stringDate) == 8 and NewString == '' :     
        YYYY = int(stringDate[:4])
        MM = int(stringDate[4:6])
        DD = int(stringDate[-2:])
        if YYYY >= 1900 and YYYY <= CurrentYear :
            if MM > 0 and MM <=12 :
                if DD > 0 and DD <= 31 :
                    NewString = stringDate
                    
    # check DDMMYYYY
    if len(stringDate) == 8 and NewString == '' :  
        YYYY = int(stringDate[-4:])
        MM = int(stringDate[2:4])
        DD = int(stringDate[:2])
        if YYYY >= 1900 and YYYY <= CurrentYear :
            if MM > 0 and MM <=12 :
                if DD > 0 and DD <= 31 :
                    NewString = str(YYYY) + str(MM) + str(DD)
                    print('--- the date format converted from DDMMYYYY to YYYYMMDD:\n    '+stringDate+' → '+NewString)
  
    # check MMDDYYYY
    if len(stringDate) == 8 and NewString == '' :  
        YYYY = int(stringDate[-4:])
        MM = int(stringDate[:2])
        DD = int(stringDate[2:4])
        if YYYY >= 1900 and YYYY <= CurrentYear :
            if MM > 0 and MM <=12 :
                if DD > 0 and DD <= 31 :
                    NewString = str(YYYY) + str(MM) + str(DD)
                    print('--- the date format converted from MMDDYYYY to YYYYMMDD:\n    '+stringDate+' → '+NewString)
    
    if NewString == '' :
        try:
            NewString = strDate( stringDate , formatOUT='YYYYMMDD')
        except :
            NewString = ''
    
    if not returnString :
        return NewString == stringDate
    else : # returnString == True
        return NewString
