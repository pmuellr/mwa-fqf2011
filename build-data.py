#!/usr/bin/env python

import os
import re
import sys
import json

DEBUG = True

#--------------------------------------------------------------------
def main():

    input = sys.stdin.read()
    result = parseData(input)
    result = json.dumps(result, indent=3)
    
    print "var EventData = %s" % result

#--------------------------------------------------------------------
def checkData(data):
    return data
    
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
    
    result = {
        "events": parseEventData(eventData),
        "bands":  parseBandData(bandData),
        "venues": parseVenueData(venueData),
    }
    
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
            event = {}
            events.append(event)
            event["band"] = val
            
        if key == "date":
            (date, time, len) = val.split(None, 2)
            len = int(len)
            event["date"] = date
            event["time"] = time
            event["len"]  = len
            
        if key == "venue":
            event["venue"] = val
        
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
            band = {}
            bands.append(band)
            band["name"]  = val
            band["links"] = []
            band["desc"]  = []
            inDesc = False
            
        if inDesc:
            band["desc"].append(line)
            continue
            
        if key == "link":
            if val.strip() != "":
                band["links"].append(val)
            
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
            venue = {}
            venues.append(venue)
            venue["name"] = val
            
        if key == "number":
            venue["number"] = val
            
        if key == "color":
            venue["color"] = val
        
    return venues

#--------------------------------------------------------------------
def log(message):
    print >>sys.stderr, message

#--------------------------------------------------------------------
main()