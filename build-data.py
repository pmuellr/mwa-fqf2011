#!/usr/bin/env python

import os
import re
import sys
import json
import datetime
import urlparse

DEBUG = not True

#--------------------------------------------------------------------
def main():

    input = sys.stdin.read()
    result = parseData(input)
    result = json.dumps(result, indent=3)
    
    print "var EventData = %s" % result

#--------------------------------------------------------------------
def parseData(input):
    patternComment = re.compile(r"^\s*#.*$", re.MULTILINE)
    input = patternComment.sub("", input)

    patternParts = re.compile(r".*^events:$(.*)^bands:$(.*)^venues:$(.*)", re.MULTILINE | re.DOTALL)
    match = patternParts.match(input)
    
    if not match:
        print >>sys.stderr, "error"
        sys.exit()

    eventData = match.group(1)
    bandData  = match.group(2)
    venueData = match.group(3)
    
    result = JSDict()
    result.events = parseEventData(eventData)
    result.bands  = parseBandData(bandData)
    result.venues = parseVenueData(venueData)
    
    return checkData(result)

#--------------------------------------------------------------------
# event: Benny Grunch & the Bunch
# date:  2011/04/08 11:00 90
# venue: 1
#--------------------------------------------------------------------
def parseEventData(input):
    lines = [line.strip() for line in input.split("\n")]

    events = []
    event = None
    
    for line in lines:
        if line == "": continue
        if DEBUG: log("processing: %s" % line)
        
        (key, val) = line.split(":",1)
        key = key.strip()
        val = val.strip()
        
        if key == "event":
            event = JSDict()
            events.append(event)
            event.band = val
            
        if key == "date":
            (date, time, len) = val.split(None, 2)
            
            len = intVal(len)
            if None == len:
                error("length not numeric in: '%s'" % line)
                sys.exit(1)
                
            event.date = date
            event.time = time
            event.len  = len
            
        if key == "venue":
            event.venue = val
        
    return events

#--------------------------------------------------------------------
# band: Zydepunks
# link:
# desc:
#--------------------------------------------------------------------
def parseBandData(input):
    lines = [line.strip() for line in input.split("\n")]
    
    bands = []
    band  = None
    
    inDesc = False
    
    for line in lines:
        if line == "": continue
        if DEBUG: log("processing: %s" % line)

        parts = line.split(":",1)
        key = None
        val = None
        if len(parts) == 2:
            key = parts[0].strip()
            val = parts[1].strip()
        
        if key == "band":
            band = JSDict()
            bands.append(band)
            band.name  = val
            band.links = []
            band.desc  = []
            inDesc = False
            
        if inDesc:
            band.desc.append(line)
            continue
            
        if key == "link":
            if val.strip() != "":
                band.links.append(val)
            
        if key == "desc":
            inDesc = True

    return bands

#--------------------------------------------------------------------
# venue:  Jackson Square
# number: 1
# color:  39c b
#--------------------------------------------------------------------
def parseVenueData(input):
    lines = [line.strip() for line in input.split("\n")]

    venues = []
    venue = None
    
    for line in lines:
        if line == "": continue
        if DEBUG: log("processing: %s" % line)
        
        (key, val) = line.split(":",1)
        key = key.strip()
        val = val.strip()
        
        if key == "venue":
            venue = JSDict()
            venues.append(venue)
            venue.name = val
            
        if key == "number":
            venue.number = val
            
        if key == "color":
            venue.color = val
        
    return venues

#--------------------------------------------------------------------
def checkData(data):
    tables = JSDict()
    tables.bands  = {}
    tables.venues = {}
    
    for band in data.bands:
        tables.bands[band.name] = band
        
    for venue in data.venues:
        tables.venues[venue.number] = venue
    
    checkEventData(data.events, tables)
    checkBandData(data.bands)
    checkVenueData(data.venues)
    return data

#--------------------------------------------------------------------
# date:  "2011/04/08"
# band:  "Benny Grunch & the Bunch"
# venue: "1"
# len:   90
# time:  "11:00"
#--------------------------------------------------------------------
def checkEventData(data, tables):
    for event in data:
        item = "event: date: '%s', band: '%s', time: '%s'" % (event.date, event.band, event.time)
        
        yy  = intVal(event.date[0:4])
        mm  = intVal(event.date[5:7])
        dd  = intVal(event.date[8:10])
        hhh = intVal(event.time[0:2])
        mmm = intVal(event.time[3:5])
        
        if event.band == "": error("invalid band for %s" % item)
        
        if None == yy:  error("invalid year in date for %s" % item)
        if None == mm:  error("invalid month in date for %s" % item)
        if None == dd:  error("invalid day in date for %s" % item)
        if None == hhh: error("invalid hour in time for %s" % item)
        if None == mmm: error("invalid minute in time for %s" % item)
        
        if yy < 2011: error("invalid year in date for %s" % item)
        if mm < 1:    error("invalid month in date for %s" % item)
        if mm > 12:   error("invalid month in date for %s" % item)
        if dd < 1:    error("invalid day in date for %s" % item)
        if dd > 31:   error("invalid day in date for %s" % item)
            
        try:
            datetime.date(yy, mm, dd)
        except:
            error("invalid day in date for %s" % item)
            
        if event.venue not in tables.venues: error("invalid venue for %s" % item)
        if event.band  not in tables.bands:  error("invalid band for %s" % item)
        
        if event.len < 0:   error("invalid length for %s" % item)
        if event.len > 240: error("invalid length for %s" % item)
    
#--------------------------------------------------------------------
# name: "Benny Grunch & the Bunch", 
# links: ["http://www.bennygrunch.com/"]
# desc: [ "line1", "line2" ]
#--------------------------------------------------------------------
def checkBandData(data):
    
    for band in data:
        item = "band: '%s'" % (band.name)
        
        if band.name == "": error("invalid band for %s" % item)
        
        for link in band.links:
            urlParts = urlparse.urlparse(link)
            if urlParts[0] == "": error("invalid scheme in link for %s" % item)
            if urlParts[1] == "": error("invalid host in link for %s" % item)
            
        
#--------------------------------------------------------------------
# color:  "969"
# name:   "500 Royal"
# number: "16"
#--------------------------------------------------------------------
colorPattern = re.compile(r"[0-9A-F][0-9A-F][0-9A-F]")
def checkVenueData(data):
    for venue in data:
        item = "venue: '%s'" % (venue.name)
        
        if venue.name == "": error("invalid name for %s" % item)
        number = intVal(venue.number)
        if not number:  error("invalid number for %s" % item)
        if number < 1:  error("invalid number for %s" % item)
        if number > 20: error("invalid number for %s" % item)
        
        venue.color = venue.color.upper()
        
        if not colorPattern.match(venue.color): error("invalid color for %s" % item)

#--------------------------------------------------------------------
def intVal(string):
    if string == "0":  return 0
    if string == "00": return 0
    
    try:
        return int(string.lstrip("0"))
    except:
        return None

#--------------------------------------------------------------------
def error(message):
    log("ERROR: %s" % message)
    sys.exit(1)

#--------------------------------------------------------------------
def log(message):
    print >>sys.stderr, message

#--------------------------------------------------------------------
class JSDict(dict):
    def __init__(self):
        dict.__init__(self)
    
    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value
    
    
#--------------------------------------------------------------------
main()