#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 12:42:50 2020

@author: martin
"""

__version__ = '0.0.20-11-01'
__all__ = ['gpx']

from geopy.geocoders import Nominatim
import pandas as pd
from numpy import linspace
from datafiletoolbox import strDate
from datafiletoolbox import extension

geolocator = Nominatim(user_agent="MyPhotoTracks")

class gpx(object) :
    """
    A class to simplify reading a GPX file.
    It extracts only the latitude, longitude and time.
    
    Available properties and methods() :
        .load( path_to_gpx_file ) method to load a .gpx file overwritting any previously read gpx
        
        .start property returns the first time in the gpx track
        .end property returns the last time in the gpx track
        
        .DF property returns a Pandas DataFrame with latitude, longitude and time
        
        .country property returns the country where the track is located
        .county property returns the county where the track is located
        .city property returns the city where the track is located
        NB: if the track pass through more than one city or county, the most common one is returned
        
        .counties() method returns all the counties where the track pass by
        .cities() method returns all the cities where the track pass by
        
    """
    
    def __init__(self,filepath) :
        self.filepath = filepath
        self.string = None
        self.version = None
        self.metadata = []
        self.tracks = {}
        self.load(self.filepath)
        self.location = {}
    
    def __len__(self) :
        output = {}
        for trackcount in self.tracks :
            output[trackcount] = max( len(self.tracks[trackcount]['lat']) , len(self.tracks[trackcount]['lon']) , len(self.tracks[trackcount]['ele']) , len(self.tracks[trackcount]['time'])  ) 
        return output
    
    def load(self,filepath) :
        f = open(self.filepath,'r') 
        self.string = f.readlines()
        f.close()
        
        self.name = extension(filepath)[1]
        
        lines = []
        for line in self.string :
            if '><' not in line :
                lines.append( line )
            else :
                newlines = []
                while '><' in line :
                    newlines.append( line[:line.index('><')+1] )
                    line = line[ line.index('><')+1: ]
                lines += newlines
        self.string = lines
        
        trackcount = -1
        self.tracks = { -1 : {'lat':[],
                              'lon':[],
                              'ele':[],
                              'time':[]}
                       }
        
        for line in self.string :
            line = line.strip()
            if 'version=' in line :
                for part in line.split() :
                    if len(part)>8 and part[:8] == 'version=' :
                        self.version = part[8:].strip('"')
                        break
            
            elif line == '<trkseg>' :
                trackcount += 1
                self.tracks[trackcount] = {'lat':[],
                                     'lon':[],
                                     'ele':[],
                                     'time':[]}
            elif line[:6] == '<trkpt' :
                for part in line.split() :
                    if part[:4] == 'lat=' :
                        self.tracks[trackcount]['lat'].append( float( part[4:].strip(' "<>\n') ) )
                    elif part[:4] == 'lon=' :
                        self.tracks[trackcount]['lon'].append( float( part[4:].strip(' "<>\n') ) ) 
            elif line[:5] == '<ele>' :
                self.tracks[trackcount]['ele'].append( float( line.strip(' </ele>\n') ) )
            elif line[:6] == '<time>' :
                self.tracks[trackcount]['time'].append( line.strip(' </time>\n') )
            elif line.strip() == '</trkpt>' :
                self.checkLen(trackcount)
            elif line.strip() == '</trkseg>' :
                self.checkLen(trackcount)
    
    def checkLen(self,count=None) :
        if count is None :
            count = list(range(len(self.tracks)))
        else :
            count = [ count ]
        for c in count :
            N = max( len(self.tracks[c]['lat']) , len(self.tracks[c]['lon']) , len(self.tracks[c]['ele']) , len(self.tracks[c]['time'])  ) 
            for att in ['lat','lon','ele','time'] :
                while N > len(self.tracks[c][att]) :
                    self.tracks[c][att].append(None)
    
    @property
    def start(self) :
        if len(self.DF) > 0 :
            return self.DF.time.iloc[0]
        if len(self.tracks) > 0 :
            for each in self.tracks.keys() :
                if len( self.tracks[each]['time'] ) > 0 :
                    return pd.to_datetime( self.tracks[each]['time'][0] , format='%Y-%m-%dT%H:%M:%S' )
    
    @property
    def end(self) :
        if len(self.DF) > 0 :
            return self.DF.time.iloc[-1]
        if len(self.tracks) > 0 :
            for each in list(self.tracks.keys())[::-1] :
                if len( self.tracks[each]['time'] ) > 0 :
                    return pd.to_datetime( self.tracks[ each ]['time'][-1] , format='%Y-%m-%dT%H:%M:%S' )

    @property 
    def date(self) :
        if self.start.date() != self.end.date() :
            print( ' start and end are different:\n   start: ' + str(self.start) + '\n     end: ' + str(self.end) )
        return strDate( self.start.date() , formatIN='YYYY-MM-DD' , formatOUT='YYYY-MM-DD' )
    
    @property
    def DF(self) :
        DF = {'time':[],
              'lat':[],
              'lon':[],
              'ele':[]}
        for track in self.tracks :
            if track >= 0 :
                for key in DF.keys() :
                    DF[key] += self.tracks[track][key] 
        DF = pd.DataFrame(DF)
        DF['time'] = pd.to_datetime(DF['time'],format='%Y-%m-%dT%H:%M:%S')    
        return DF
    
    def mean(self) :
        return self.DF['lat'].mean() , self.DF['lon'].mean()
    
    def percentile(self,perc=50) :
        if perc > 1 :
            perc = perc/100
        return self.DF['lat'].quantile(perc) , self.DF['lon'].quantile(perc)
    
    def getLocation(self,lat=None,lon=None) :
        if type(lat) is tuple and len(lat)==2 and lon is None:
            lon = lat[1]
            lat = lat[0]
        if lat is None :
            lon = self.mean()[0]
        if lon is None :
            lon = self.mean()[1]
        if (lat,lon) not in self.location :
            # geolocator = Nominatim(user_agent="MyPhotoTracks")
            try :
                self.location[(lat,lon)] = geolocator.reverse( str(lat) + ', ' + str(lon) )
            except :
                self.location[(lat,lon)]= None
        return self.location[(lat,lon)]
    
    @property
    def city(self) :
        if len(set( self.cities() )) == 1 :
            if '/' in self.cities()[0] :
                return self.cities()[0].split('/')[0].strip()
            return self.cities()[0]
        elif len( self.cities() ) > 2 :
            most = max(set(self.cities()), key = self.cities().count)
            if round( self.cities().count(most) / len(self.cities()) , 2 ) >= 2/3 :
                if '/' in most :
                    return most.split('/')[0].strip()
                return most
        elif len( self.cities() ) == 2 :
            if len(set( self.counties() )) == 1 :
                if self.counties()[0] in self.cities() :
                    if '/' in self.counties()[0] :
                        return self.counties()[0].split('/')[0].strip()
                    return self.counties()[0]
        elif len( self.cities() ) == 0 :
            if len(set( self.counties() )) == 1 :
                if '/' in self.counties()[0] :
                    return self.counties()[0].split('/')[0].strip()
                return self.counties()[0]
            

    def cities(self) :
        cities = []
        counties = []
        for P in [0.01] + list(linspace(0.05,0.95,19).round(2)) + [0.99] :
            if self.getLocation( self.percentile(P) ) is not None :
                if 'address' in self.getLocation( self.percentile(P) ).raw :
                    if 'city' in self.getLocation( self.percentile(P) ).raw['address'] :
                        cities.append( self.getLocation( self.percentile(P) ).raw['address']['city'] )
        while None in cities :
            cities.pop( cities.index(None) )
        return cities
    
    def counties(self) :
        counties = []
        for P in [0.01] + list(linspace(0.05,0.95,19).round(2)) + [0.99] :
            if self.getLocation( self.percentile(P) ) is not None :
                if 'address' in self.getLocation( self.percentile(P) ).raw :
                    if 'county' in self.getLocation( self.percentile(P) ).raw['address'] :
                        counties.append( self.getLocation( self.percentile(P) ).raw['address']['county'] )
        while None in counties :
            counties.pop( counties.index(None) )
        return counties

    @property
    def county(self) :
        if len(set( self.counties() )) == 1 :
            if '/' in self.counties()[0] :
                return self.counties()[0].split('/')[0].strip()
            return self.counties()[0]
        elif len( self.counties() ) > 2 :
            most = max(set(self.counties()), key = self.counties().count)
            if '/' in most :
                return most.split('/')[0].strip()
            return most

    @property
    def country(self) :
        if self.getLocation() is not None :
            if 'address' in self.getLocation().raw :
                if 'country' in self.getLocation().raw['address'] :
                    return self.getLocation().raw['address']['country']
        else :
            for P in [0.01] + list(linspace(0.05,0.95,19).round(2)) + [0.99] :
                if self.getLocation( self.percentile(P) ) is not None :
                    if 'address' in self.getLocation( self.percentile(P) ).raw :
                        if 'country' in self.getLocation( self.percentile(P) ).raw['address'] :
                            return self.getLocation( self.percentile(P) ).raw['address']['country']
        
        
