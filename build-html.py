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
    readFile()
    body = generateBody()
    writeHtml(body)

#--------------------------------------------------------------------
def readFile():
    content = sys.stdin.read()
    parseData(content)
    
#--------------------------------------------------------------------
def generateBody():
    return ""

#--------------------------------------------------------------------
def writeHtml(body):
    print "%s%s%s" % (getHtmlHead(), body, getHtmlTail())

#--------------------------------------------------------------------
class Event:
    events = []

    #----------------------------------------------------------------
    @staticmethod
    def getEvents():
        return Event.events[:]

    #----------------------------------------------------------------
    def __init__(self, venue, date, timeS, timeSampm, timeE, timeEampm, band):
        self.venue     = venue
        self.date      = date
        self.timeS     = timeS
        self.timeSampm = timeS
        self.timeE     = timeE
        self.timeEampm = timeE
        self.band      = band
        
        Event.events.append(self)

#--------------------------------------------------------------------
class Band:
    bands = {}

    #----------------------------------------------------------------
    @staticmethod
    def getBands():
        return Band.bands.values()

    #----------------------------------------------------------------
    @staticmethod
    def getBand(bandName):
        return Band.bands.get(bandName)

    #----------------------------------------------------------------
    def __init__(self, name):
        self.name  = name
        self.links = []
        self.desc  = []
        
        Band.bands[name] = self
        
#--------------------------------------------------------------------
class Venue:
    venues = {}

    #----------------------------------------------------------------
    @staticmethod
    def getVenues():
        return Venue.venues.values()

    #----------------------------------------------------------------
    @staticmethod
    def getVenue(number):
        return Venue.venues.get(number)

    #----------------------------------------------------------------
    def __init__(self, name, number, color):
        self.name   = name
        self.number = number
        self.color  = color
        
        Venue.venues[number] = self

#--------------------------------------------------------------------
def parseData(input):
    patternComment = re.compile(r"^\s*#.*$", re.MULTILINE)
    input = patternComment.sub("", input)

    patternParts = re.compile(r".*^events:$(.*)^bands:$(.*)^venues:$(.*)", re.MULTILINE | re.DOTALL)
    match = patternParts.match(input)
    
    if not match: error("basic structure wrong for file")

    eventData = match.group(1)
    bandData  = match.group(2)
    venueData = match.group(3)
    
    parseEventData(eventData)
    parseBandData(bandData)
    parseVenueData(venueData)
    
    validateData()

#--------------------------------------------------------------------
# 15  2011/04/09  11:00 AM    12:15 PM    Alex Bosworth
#--------------------------------------------------------------------
def parseEventData(input):
    lines = [line.strip() for line in input.split("\n")]
    lines = [line for line in lines if line != ""]

    for line in lines:
        if DEBUG: log("processing: %s" % line)
        
        parts = line.split(None, 6)
        if len(parts) != 7: error("event line invalid: %s" % line)
            
        venue     = parts[0].upper()
        date      = parts[1]
        timeS     = parts[2]
        timeSampm = parts[3].lower()
        timeE     = parts[4]
        timeEampm = parts[5].lower()
        band      = parts[6]
        
        Event(venue, date, timeS, timeSampm, timeE, timeEampm, band)

#--------------------------------------------------------------------
# band: Zydepunks
# link:
# desc:
#--------------------------------------------------------------------
def parseBandData(input):
    lines = [line.strip() for line in input.split("\n")]
    lines = [line for line in lines if line != ""]
    
    inDesc = False
    band   = None
    
    for line in lines:
        if DEBUG: log("processing: %s" % line)

        parts = line.split(":",1)
        key = None
        val = None
        if len(parts) == 2:
            key = parts[0].strip()
            val = parts[1].strip()
        
        if key == "band":
            band = Band(val)
            inDesc = False
            
        if inDesc:
            band.desc.append(line)
            continue
            
        if key == "link":
            if val.strip() != "":
                band.links.append(val)
            
        if key == "desc":
            inDesc = True

#--------------------------------------------------------------------
#  1  39c  Jackson Square 
#--------------------------------------------------------------------
def parseVenueData(input):
    lines = [line.strip() for line in input.split("\n")]
    lines = [line for line in lines if line != ""]

    for line in lines:
        if DEBUG: log("processing: %s" % line)
        
        parts = line.split(None, 2)
        if len(parts) != 3: error("venue line invalid: %s" % line)
            
        number    = parts[0].upper()
        color     = parts[1].lower()
        name      = parts[2]

        Venue(name, number, color)

#--------------------------------------------------------------------
def validateData():
    events = Event.getEvents()
    
    errors = False
    for event in events:
        venue = Venue.getVenue(event.venue)
        band  = Band.getBand(event.band)
        
        if None == venue: 
            log("ERROR: event with unknown venue: %s" % event.venue)
            errors = True
            
        if None == band:  
            # log("ERROR: event with unknown band: %s"  % event.band)
            errors = True
            
    if errors:
        error("stopping because of errors")

#--------------------------------------------------------------------
def error(message):
    log("ERROR: %s" % message)
    sys.exit(1)

#--------------------------------------------------------------------
def log(message):
    print >>sys.stderr, message

#--------------------------------------------------------------------
def getHtmlHead():
    return """<!DOCTYPE html>

<!-- ========================================================================
Copyright (c) 2011 Patrick Mueller
Licensed under the MIT license: 
http://www.opensource.org/licenses/mit-license.php
======================================================================== -->

<html not-a-manifest="index.manifest">

<!-- ======================================================================== -->
<head>
<title>mwa-fqf2011</title>

<!-- debug -->

<!-- full URLs since that's all Android will accept -->
<link rel="shortcut icon"                                href="http://muellerware.org/mwa-fqf-2011/images/mwa-fqf2011-desktop-57x57.png" />
<link rel="apple-touch-icon-precomposed"                 href="http://muellerware.org/mwa-fqf-2011/images/mwa-fqf2011-desktop-57x57.png"/>
<link rel="apple-touch-icon-precomposed" sizes="57x57"   href="http://muellerware.org/mwa-fqf-2011/images/mwa-fqf2011-desktop-57x57.png"/>
<link rel="apple-touch-icon-precomposed" sizes="72x72"   href="http://muellerware.org/mwa-fqf-2011/images/mwa-fqf2011-desktop-72x72.png"/>
<link rel="apple-touch-icon-precomposed" sizes="114x114" href="http://muellerware.org/mwa-fqf-2011/images/mwa-fqf2011-desktop-114x114.png"/>

<meta name="apple-mobile-web-app-capable" content="yes" />
<meta name="viewport" content="initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no, width=device-width">

<link rel="stylesheet" href="css/mwa-fqf2011.css"/>

<script src="vendor/zepto/zepto.js"></script>
<script src="vendor/underscore/underscore.js"></script>
<script src="vendor/modjewel/modjewel-require.js"></script>

<script src="vendor/scooj/scooj.transportd.js"></script>
<script src="modules/common/StackTrace.transportd.js"></script>
<script src="modules/mwa/fqf2011/DB.transportd.js"></script>
<script src="modules/mwa/fqf2011/Main.transportd.js"></script>

<script src="vendor/zepto/zepto.js"></script>

<script src="data.js"></script>

<script>
function main() { require("mwa/fqf2011/Main").main() }

$(document).ready(main)
</script>

</head>

<!-- ======================================================================= -->
<body>
"""

#--------------------------------------------------------------------
def getHtmlTail():
    return """
<!-- ======================================================================= -->
</body>
</html>
"""

#--------------------------------------------------------------------
main()