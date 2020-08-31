# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 00:17:46 2020

@author: MCARAYA
"""

__version__ = '0.5.20-06-05'

from metadataDL.validate import characters
from metadataDL.filehandling.filepaths import extension
import pandas as pd

class NotUniqueError(Exception) :
    pass
class WellNotFoundError(Exception) :
    pass

DataPreparationRoot = '_STAGING'

# url = r'http://srv02550/ReportServer/Reserved.ReportViewerWebControl.axd?ExecutionID=riwxob45hgavdc45brsaccj5&Culture=3082&CultureOverrides=False&UICulture=10&UICultureOverrides=False&ReportStack=1&ControlID=7ca5756a56be45dab9d105c668132a4f&OpType=Export&FileName=Well+Geographic+Hierarchy+New&ContentDisposition=OnlyHtmlInline&Format=CSV'
url = r'//danas/Dig_Trans_Proj/DATALAKE_EP_PRE_INGESTION/Z_LOGS_RESULTS/WellHierarchy.csv'


class WELL_GEOGRAPHIC_HIERARCHY(object) :
    def __init__(self,csv) :
        self.loadCSV(csv)
    
    def loadCSV(self,csv) :
        self.wgh = pd.read_csv(csv)
    
    def get_DataFrame(self) :
        return self.wgh.copy()
    
    @property
    def dataframe(self) :
        return self.get_DataFrame()
    @property
    def df(self) :
        return self.get_DataFrame()
    
    def get_colum(self,ReturnColumn,UWI=None,CEPSA_STANDARD_NAME=None,CONTINENT_NAME=None,COUNTRY_NAME=None,BASIN_NAME=None,CLOSURE_NAME=None) :
        df = self.wgh.copy()
        if UWI is not None :
            df = df[df['UWI']==UWI]
        if CEPSA_STANDARD_NAME is not None :
            df = df[df['CEPSA_STANDARD_NAME']==CEPSA_STANDARD_NAME]
        if CONTINENT_NAME is not None :
            df = df[df['CONTINENT_NAME']==CONTINENT_NAME]
        if BASIN_NAME is not None :
            df = df[df['BASIN_NAME']==BASIN_NAME]
        if CLOSURE_NAME is not None :
            df = df[df['CLOSURE_NAME']==CLOSURE_NAME]
        return df[ReturnColumn]

    def UWI_or_CEPSA_STANDARD_NAME(self,UWI_or_CEPSA_STANDARD_NAME) :
        if UWI_or_CEPSA_STANDARD_NAME in self.wgh['UWI'].array :
            UWI=UWI_or_CEPSA_STANDARD_NAME
            CEPSA_STANDARD_NAME=None
            UwiOrName = 'UWI'
        elif UWI_or_CEPSA_STANDARD_NAME in self.wgh['CEPSA_STANDARD_NAME'].array :
            UWI=None
            CEPSA_STANDARD_NAME=UWI_or_CEPSA_STANDARD_NAME
            UwiOrName = 'CEPSA_STANDARD_NAME'
        else :
            UWI=None
            CEPSA_STANDARD_NAME=None
            UwiOrName = None
        return ( UwiOrName , UWI , CEPSA_STANDARD_NAME )
        
    def get_country(self,UWI_or_CEPSA_STANDARD_NAME,*,CONTINENT_NAME=None,COUNTRY_NAME=None,BASIN_NAME=None,CLOSURE_NAME=None) :
        ReturnColumn = 'COUNTRY_NAME'
        UwiOrName , UWI , CEPSA_STANDARD_NAME = self.UWI_or_CEPSA_STANDARD_NAME(UWI_or_CEPSA_STANDARD_NAME)
        output = self.get_colum(ReturnColumn,UWI=UWI,CEPSA_STANDARD_NAME=CEPSA_STANDARD_NAME,CONTINENT_NAME=CONTINENT_NAME,COUNTRY_NAME=COUNTRY_NAME,BASIN_NAME=BASIN_NAME,CLOSURE_NAME=CLOSURE_NAME)
        if UwiOrName is None :
            print(' WARNING: the well name ' + UWI_or_CEPSA_STANDARD_NAME + ' does not match any UWI or CEPSA_STANDARD_NAME')
            return None
        if len(output) == 1 :
            return output.array[0]
        elif len(output) == 0 :
            return ''
        else :
            print(' WARNING: not unique solution for the ' + UwiOrName + ': ' + UWI_or_CEPSA_STANDARD_NAME )
            return output.array
        
    def get_basin(self,UWI_or_CEPSA_STANDARD_NAME,*,CONTINENT_NAME=None,COUNTRY_NAME=None,BASIN_NAME=None,CLOSURE_NAME=None) :
        ReturnColumn = 'BASIN_NAME'
        UwiOrName , UWI , CEPSA_STANDARD_NAME = self.UWI_or_CEPSA_STANDARD_NAME(UWI_or_CEPSA_STANDARD_NAME)
        output = self.get_colum(ReturnColumn,UWI=UWI,CEPSA_STANDARD_NAME=CEPSA_STANDARD_NAME,CONTINENT_NAME=CONTINENT_NAME,COUNTRY_NAME=COUNTRY_NAME,BASIN_NAME=BASIN_NAME,CLOSURE_NAME=CLOSURE_NAME)
        if UwiOrName is None :
            print(' WARNING: the well name ' + UWI_or_CEPSA_STANDARD_NAME + ' does not match any UWI or CEPSA_STANDARD_NAME')
            return None
        if len(output) == 1 :
            return output.array[0]
        elif len(output) == 0 :
            return ''
        else :
            print(' WARNING: not unique solution for the ' + UwiOrName + ': ' + UWI_or_CEPSA_STANDARD_NAME )
            return output.array
    
    def get_wellname(self,UWI_or_CEPSA_STANDARD_NAME,*,CONTINENT_NAME=None,COUNTRY_NAME=None,BASIN_NAME=None,CLOSURE_NAME=None) :
        ReturnColumn = 'CEPSA_STANDARD_NAME'
        UwiOrName , UWI , CEPSA_STANDARD_NAME = self.UWI_or_CEPSA_STANDARD_NAME(UWI_or_CEPSA_STANDARD_NAME)
        output = self.get_colum(ReturnColumn,UWI=UWI,CEPSA_STANDARD_NAME=CEPSA_STANDARD_NAME,CONTINENT_NAME=CONTINENT_NAME,COUNTRY_NAME=COUNTRY_NAME,BASIN_NAME=BASIN_NAME,CLOSURE_NAME=CLOSURE_NAME)
        if UwiOrName is None :
            print(' WARNING: the well name ' + UWI_or_CEPSA_STANDARD_NAME + ' does not match any UWI or CEPSA_STANDARD_NAME')
            return None
        if len(output) == 1 :
            return output.array[0]
        elif len(output) == 0 :
            return ''
        else :
            print(' WARNING: not unique solution for the ' + UwiOrName + ': ' + UWI_or_CEPSA_STANDARD_NAME )
            return output.array

    def get_closure(self,UWI_or_CEPSA_STANDARD_NAME,*,CONTINENT_NAME=None,COUNTRY_NAME=None,BASIN_NAME=None,CLOSURE_NAME=None) :
        ReturnColumn = 'CLOSURE_NAME'
        UwiOrName , UWI , CEPSA_STANDARD_NAME = self.UWI_or_CEPSA_STANDARD_NAME(UWI_or_CEPSA_STANDARD_NAME)
        output = self.get_colum(ReturnColumn,UWI=UWI,CEPSA_STANDARD_NAME=CEPSA_STANDARD_NAME,CONTINENT_NAME=CONTINENT_NAME,COUNTRY_NAME=COUNTRY_NAME,BASIN_NAME=BASIN_NAME,CLOSURE_NAME=CLOSURE_NAME)
        if UwiOrName is None :
            print(' WARNING: the well name ' + UWI_or_CEPSA_STANDARD_NAME + ' does not match any UWI or CEPSA_STANDARD_NAME')
            return None
        if len(output) == 1 :
            return output.array[0]
        elif len(output) == 0 :
            return ''
        else :
            print(' WARNING: not unique solution for the ' + UwiOrName + ': ' + UWI_or_CEPSA_STANDARD_NAME )
            return output.array
        

WGH = WELL_GEOGRAPHIC_HIERARCHY(url)


def PRE_INGESTION(wellname,country=None):
    """
    given a wellname, and optionaly the country, 
    returns the corresponding fullpath in PRE_INGESTION structure.
    """  
    if country is None :
        country = WGH.get_country(wellname)
    if country is None : # WGH returned None
        raise WellNotFoundError(' WARNING: the well name ' + wellname + ' does not match any UWI or CEPSA_STANDARD_NAME')
    if type(country) is str :
        basin = WGH.get_basin(wellname,COUNTRY_NAME=country)
        closure = WGH.get_closure(wellname,COUNTRY_NAME=country)
        wellname = WGH.get_wellname(wellname,COUNTRY_NAME=country)
    else :
        raise NotUniqueError(' not unique solution for the wellname :' + wellname )

    return '//danas/Dig_Trans_Proj/DATALAKE_EP_PRE_INGESTION/' + \
           characters(country,True) + '/' + \
           characters(basin,True) + '/' + \
           characters(closure,True) + '/' + \
           characters(wellname,True) + '/'


# def STAGING(STAGINGPath,*,CountryLevel=None,WellLevel=None,DataTypeLevel=None) :
def STAGING(STAGINGPath,*,WellLevel=None,DataTypeLevel=None) :
    # if CountryLevel is None :
    #     try :
    #         CountryLevel = countryLevel
    #     except :
    #         try:
    #             CountryLevel = STAGINGPath.split('/').index(DataPreparationRoot) +1
    #         except :
    #             raise TypeError(' missing CountryLevel argument')
    STAGINGPath = extension(STAGINGPath)[3]
    # print('staggin path:\n' + STAGINGPath)
    # print('well level ' + str(WellLevel))
    if WellLevel is None :
        try :
            # print('well level 1 ')
            WellLevel = wellLevel
            # print('well level 1 ' + str(WellLevel))
        except :
            try:
                # print('well level try')
                # print(str(DataPreparationRoot))
                # print(type(STAGINGPath.split('/').index(DataPreparationRoot)),STAGINGPath.split('/').index(DataPreparationRoot))
                WellLevel = STAGINGPath.split('/').index(DataPreparationRoot) +3
                # print('well level 2 ' + str(WellLevel))
            except :
                raise TypeError(' missing WellLevel argument')
    if DataTypeLevel is None :
        try :
            DataTypeLevel = dataTypeLevel
        except :
            try:
                DataTypeLevel = STAGINGPath.split('/').index(DataPreparationRoot) +4
            except :
                raise TypeError(' missing DataTypeLevel argument')
    # country = STAGINGPath.split('/')[ CountryLevel ].upper()
    wellname = STAGINGPath.split('/')[ WellLevel ].upper()
    dataType = STAGINGPath.split('/')[ DataTypeLevel ].upper()
    return (wellname , dataType)


def PRE_INGESTION_parts(PRE_INGESTION_path) :
    PRE_INGESTION_path = extension(PRE_INGESTION_path)[3]
    if not PRE_INGESTION_path.startswith( '//danas/Dig_Trans_Proj/DATALAKE_EP_PRE_INGESTION/' ) :
        print(PRE_INGESTION_path + '\n is not a PRE_INGESTION path.')
        return None
    PRE_INGESTION_path = PRE_INGESTION_path[ len('//danas/Dig_Trans_Proj/DATALAKE_EP_PRE_INGESTION/') : ].split('/')
    return { 'Country' : PRE_INGESTION_path[0] ,
             'Basin' : PRE_INGESTION_path[1] ,
             'Closure' : PRE_INGESTION_path[2] ,
             'Well' : PRE_INGESTION_path[3] ,
             'DataType' : PRE_INGESTION_path[4] }
    
        
    
    #\\danas\Dig_Trans_Proj\DATALAKE_EP_PRE_INGESTION\UNITED_ARAB_EMIRATES\RUB_AL_KHALI\SARB\SR-0001V\TOPS