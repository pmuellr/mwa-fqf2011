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
    return BodyGenerator().getBody()

#--------------------------------------------------------------------
def writeHtml(body):
    print "%s%s%s" % (getHtmlHead(), body, getHtmlTail())

#--------------------------------------------------------------------
class BodyGenerator:
    
    #----------------------------------------------------------------
    def __init__(self):
        self.body = []

    #----------------------------------------------------------------
    def generate(self):
        self.generateEventsPage()
        self.generateBandsPage()
        self.generateVenuesPage()
        self.generateMapPage()
        self.generateToolsPage()

    #----------------------------------------------------------------
    def generateEventsPage(self):
        self.pageSeparator()
        self.add('<div id="page-events" class="page">')
        self.pageMenu()
        self.filterMenu()

        events = Event.getEventsByTime()

        self.add('<table width="100%" cellspacing="0" cellpadding="3" rules="rows">')
        
        headerStyle = 'style="color:white; background-color:black"'
        
        lastDate = ""
        for event in events:
            if event.date != lastDate:
                self.add('<tr class="header"><td colspan="4" %s>%s - %s' % (headerStyle, event.day, event.date))
                lastDate = event.date
                
            venue = Venue.getVenue(event.venue)
            venueBackground = 'style="background-color:#%s"' % venue.color
            
            self.add('<tr>')
            self.add('<td valign="top">&#x2606;')
            self.add('<td valign="top" %s>%s' % (venueBackground, event.venue))
            self.add('<td valign="top" align="right">%s%s' % (event.timeS, event.timeSampm))
            self.add('<td valign="top">%s' % event.band)
        
        self.add('</table>')
        
        self.add('</div>')
        
    #----------------------------------------------------------------
    def generateBandsPage(self):
        self.pageSeparator()
        self.add('<div id="page-bands" class="page">')
        self.pageMenu()
        self.filterMenu()

        events = Event.getEventsByBand()

        self.add('<table width="100%" cellspacing="0" cellpadding="3" rules="rows">')
        
        for event in events:
        
            venue = Venue.getVenue(event.venue)
            venueBackground = 'style="background-color:#%s"' % venue.color
        
            self.add('<tr>')
            self.add('<td valign="top">&#x2606;')
            self.add('<td valign="top" %s>%s' % (venueBackground, event.venue))
            self.add('<td valign="top">%s' % event.day)
            self.add('<td valign="top" align="right">%s%s' % (event.timeS, event.timeSampm))
            self.add('<td valign="top">%s' % event.band)
        
        self.add('</table>')

        self.add('</div>')
        
    #----------------------------------------------------------------
    def generateVenuesPage(self):
        self.pageSeparator()
        self.add('<div id="page-venues" class="page">')
        self.pageMenu()
        self.filterMenu()

        events = Event.getEventsByVenue()

        self.add('<table width="100%" cellspacing="0" cellpadding="3" rules="rows">')
        
        lastVenue = ""
        for event in events:
            if event.venue != lastVenue:
                venue = Venue.getVenue(event.venue)
                venueName = venue.name
                venueBackground = 'style="background-color:#%s"' % venue.color
                self.add('<tr class="header"><td colspan="4" %s>%s - %s' % (venueBackground, event.venue, venueName))
                lastVenue = event.venue
                
            self.add('<tr>')
            self.add('<td valign="top">&#x2606;')
            self.add('<td valign="top">%s' % event.day)
            self.add('<td valign="top" align="right">%s%s' % (event.timeS, event.timeSampm))
            self.add('<td valign="top">%s' % event.band)
        
        self.add('</table>')

        self.add('</div>')
        
    #----------------------------------------------------------------
    def generateMapPage(self):
        self.pageSeparator()
        self.add('<div id="page-map" class="page">')
        self.pageMenu()
        self.add('<img src="images/2011-fqf-map-large.png">')
        self.add('</div>')

    #----------------------------------------------------------------
    def generateToolsPage(self):
        self.pageSeparator()
        self.add('<div id="page-tools" class="page">')
        self.pageMenu()
        self.add('<p>tools')
        self.add('</div>')

    #----------------------------------------------------------------
    def pageMenu(self):
        self.add('')
        self.add('   <div class="menu">')
        self.add('      <span class="button button-events">events</span>')
        self.add('      <span class="button button-bands">bands</span>')
        self.add('      <span class="button button-venues">venues</span>')
        self.add('      <span class="button button-map">map</span>')
        self.add('      <span class="button button-tools">+</span>')
        self.add('   </div>')
        
    #----------------------------------------------------------------
    def filterMenu(self):
        self.add('')
        self.add('   <div class="menu">')
        self.add('      <span class="toggle button-thu">thu</span>')
        self.add('      <span class="toggle button-fri">fri</span>')
        self.add('      <span class="toggle button-sat">sat</span>')
        self.add('      <span class="toggle button-sun">sun</span>')
        self.add('      <span class="toggle button-fav">&#x2605;</span>')
        self.add('   </div>')
        
    #----------------------------------------------------------------
    def pageSeparator(self):
        self.add("")
        self.add("<!-- ======================================================================= -->")
        
    #----------------------------------------------------------------
    def add(self, line):
        self.body.append(line)
    
    #----------------------------------------------------------------
    def getBody(self):
        self.generate()
        return "\n".join(self.body)
    
#--------------------------------------------------------------------
class Event:
    events = []

    #----------------------------------------------------------------
    @staticmethod
    def getEventsByTime():
        result = Event.events[:]
        result.sort(compareEventsByTime)
        return result

    #----------------------------------------------------------------
    @staticmethod
    def getEventsByBand():
        result = Event.events[:]
        result.sort(compareEventsByBand)
        return result

    #----------------------------------------------------------------
    @staticmethod
    def getEventsByVenue():
        result = Event.events[:]
        result.sort(compareEventsByVenue)
        return result

    #----------------------------------------------------------------
    def __init__(self, venue, date, timeS, timeSampm, timeE, timeEampm, band):
        self.venue     = venue
        self.date      = date
        self.timeS     = timeS
        self.timeSampm = timeSampm
        self.timeE     = timeE
        self.timeEampm = timeEampm
        self.band      = band
        
        yy = int(date[0:4])
        mm = int(date[5:7])
        dd = int(date[8:10])
        
        self.day = datetime.date(yy, mm, dd).strftime("%a")
        
        Event.events.append(self)
        
#--------------------------------------------------------------------
def compareEventsByTime(e1, e2):
    result = cmp(e1.date, e2.date)
    if result: return result
    
    result = cmp(e1.timeS + e1.timeSampm, e2.timeS + e2.timeSampm)
    if result: return result
    
    return cmp(e1.venue, e2.venue)

#--------------------------------------------------------------------
def compareEventsByBand(e1, e2):
    result = cmp(e1.band, e2.band)
    if result: return result

    result = cmp(e1.date, e2.date)
    if result: return result
    
    return cmp(e1.timeS + e1.timeSampm, e2.timeS + e2.timeSampm)

#--------------------------------------------------------------------
def compareEventsByVenue(e1, e2):
    result = cmp(e1.venue, e2.venue)
    if result: return result
    
    result = cmp(e1.date, e2.date)
    if result: return result
    
    return cmp(e1.timeS + e1.timeSampm, e2.timeS + e2.timeSampm)

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
            
        venue     = adjustVenue(parts[0].upper())
        date      = parts[1]
        timeS     = parts[2]
        timeSampm = parts[3].lower()
        timeE     = parts[4]
        timeEampm = parts[5].lower()
        band      = htmlEscape(parts[6])
        
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
            band = Band(htmlEscape(val))
            inDesc = False
            
        if inDesc:
            band.desc.append(htmlEscape(line))
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
            
        number    = adjustVenue(parts[0].upper())
        color     = parts[1].lower()
        name      = parts[2]

        Venue(name, number, color)

#--------------------------------------------------------------------
def adjustVenue(venue):
    if re.match(r"\d+", venue):
        return venue.rjust(2)
    else:
        return venue
    

#--------------------------------------------------------------------
def validateData():
    events = Event.getEventsByTime()
    
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
def htmlEscape(string):
    return string.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

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
<script src="modules/mwa-fqf2011/DB.transportd.js"></script>
<script src="modules/mwa-fqf2011/Main.transportd.js"></script>
<script src="modules/mwa-fqf2011/PageManager.transportd.js"></script>

<script src="vendor/zepto/zepto.js"></script>

<script>
require("mwa-fqf2011/Main").main()
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