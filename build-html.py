#!/usr/bin/env python

# Copyright (c) 2011 Patrick Mueller
# Licensed under the MIT license: 
# http://www.opensource.org/licenses/mit-license.php

import os
import re
import sys
import json
import datetime
import urlparse
import urllib

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
        self.generateDesc()
        self.generateMapPage()
        self.generateToolsPage()

    #----------------------------------------------------------------
    def generateEventsPage(self):
        self.pageSeparator()
        self.add('<div id="page-events" class="page">')
        self.pageMenu()
        self.filterMenu()

        events = Event.getEventsByTime()

        self.add('')
        self.add('\t<table width="100%" cellspacing="0" cellpadding="3" rules="rows">')
        
        headerStyle = 'style="color:white; background-color:black"'
        
        lastDate = ""
        for event in events:
            if event.date != lastDate:
                self.add('')
                self.add('\t\t<tr class="header"><td colspan="5" %s>%s - %s' % (headerStyle, event.day, event.date))
                self.add('')
                lastDate = event.date
                
            venue = Venue.getVenue(event.venue)
            venueBackground = 'style="background-color:#%s"' % venue.color
            
            self.add('\t\t<tr class="entry day-%s %s">' % (event.day, event.id))
            self.add('\t\t\t<td valign="top" class="fav-entry-button">&#x2606;')
            self.add('\t\t\t<td valign="top" align="right" %s>%s' % (venueBackground, event.venue))
            self.add('\t\t\t<td valign="top" align="right">%s%s&nbsp;-&nbsp' % (event.timeS, event.timeSampm))
            self.add('\t\t\t<td valign="top" colspan="2">%s' % event.band)
        
        self.add('\t</table>')
        
        self.add('</div>')
        
    #----------------------------------------------------------------
    def generateBandsPage(self):
        self.pageSeparator()
        self.add('<div id="page-bands" class="page">')
        self.pageMenu()
        self.filterMenu()

        events = Event.getEventsByBand()

        self.add('')
        self.add('\t<table width="100%" cellspacing="0" cellpadding="3" rules="rows">')
        
        for event in events:
        
            venue = Venue.getVenue(event.venue)
            venueBackground = 'style="background-color:#%s"' % venue.color
        
            self.add('\t\t<tr class="entry day-%s %s">' % (event.day, event.id))
            self.add('\t\t\t<td valign="top" class="fav-entry-button">&#x2606;')
            self.add('\t\t\t<td valign="top" align="right" %s>%s' % (venueBackground, event.venue))
            self.add('\t\t\t<td valign="top">%s' % event.day)
            self.add('\t\t\t<td valign="top" align="right">%s%s&nbsp;-&nbsp' % (event.timeS, event.timeSampm))
            self.add('\t\t\t<td valign="top">%s' % event.band)
        
        self.add('\t</table>')

        self.add('</div>')
        
    #----------------------------------------------------------------
    def generateVenuesPage(self):
        self.pageSeparator()
        self.add('<div id="page-venues" class="page">')
        self.pageMenu()
        self.filterMenu()

        events = Event.getEventsByVenue()

        self.add('')
        self.add('\t<table width="100%" cellspacing="0" cellpadding="3" rules="rows">')
        
        lastVenue = ""
        for event in events:
            if event.venue != lastVenue:
                venue = Venue.getVenue(event.venue)
                venueName = venue.name
                venueBackground = 'style="background-color:#%s"' % venue.color
                self.add('')
                self.add('\t\t<tr class="header"><td colspan="5" %s>%s - %s' % (venueBackground, event.venue, venueName))
                self.add('')
                lastVenue = event.venue
                
            self.add('\t\t<tr class="entry day-%s %s">' % (event.day, event.id))
            self.add('\t\t\t<td valign="top" class="fav-entry-button">&#x2606;')
            self.add('\t\t\t<td valign="top">%s' % event.day)
            self.add('\t\t\t<td valign="top" align="right">%s%s&nbsp;-&nbsp' % (event.timeS, event.timeSampm))
            self.add('\t\t\t<td valign="top" colspan="2">%s' % event.band)
        
        self.add('\t</table>')

        self.add('</div>')
        
    #----------------------------------------------------------------
    def generateDesc(self):
        self.pageSeparator()
        self.add('<div style="display:none;">')
        self.add('\t<table>')
        
        events = Event.getEventsByTime()
        
        for event in events:
            venue           = Venue.getVenue(event.venue)
            venueBackground = 'style="white-space:pre;padding:0 0.3em;background-color:#%s"' % venue.color
            google          = "http://google.com/search?q=%s" % (urllib.quote_plus(event.band))
        
            self.add('\t\t<tr class="desc %s">' % (event.id))
            self.add('\t\t\t<td colspan="5">')
            self.add('\t\t\t\t<p><b>%s</b>' % (event.band))
            self.add('\t\t\t\t<p><span %s>%s</span> - %s' % (venueBackground, venue.number.rjust(2), venue.name))
            self.add('\t\t\t\t<br>%s %s%s - %s%s' % (event.day, event.timeS, event.timeSampm, event.timeE, event.timeEampm))
            self.add('\t\t\t\t<p><a href="%s" target="_blank">Google Search</a>' % google)

        self.add('\t</table>')
        self.add('</div>')
        
    #----------------------------------------------------------------
    def generateMapPage(self):
        self.pageSeparator()
        self.add('<div id="page-map" class="page">')
        self.pageMenu()
        
        googleMap = "http://maps.google.com/maps/ms?ie=UTF8&hl=en&msa=0&msid=204035596704065787249.00049f838a6686caa5368&ll=29.936862,-90.104413&spn=0.025103,0.036736&z=13"
        
        self.add('\t<p>A <a target="_blank" href="%s">Google Map</a> is also available for the club listings.' % googleMap)
        self.add('\t<p><img src="images/2011-fqf-map-large.png">')
        self.add('</div>')

    #----------------------------------------------------------------
    def generateToolsPage(self):
        self.pageSeparator()
        self.add('<div id="page-tools" class="page">')
        self.pageMenu()
        
        self.add('''
<h2>Help</h2>

<p>The line of buttons along the top - events, bands, etc - switch you to 
different pages in the application.  The pages which list events contain
a list of filter buttons underneath it; by clicking a filter button, you
change whether events which match the filter are shown or not.

<p>The stars beside an event can be clicked to mark an event as a favorite.
If you've selected some favorites, a favorite filter will be available
in the filter buttons.

<p>Clicking on an entry will expand it, providing more information, or
contract it if it's expanded.

<p><a href="https://github.com/pmuellr/mwa-fqf2011">Fork me on GitHub!</a>

<h2>Diagnostics</h2>
<p>Screen dimensions: <span id="screen-width"></span> x <span id="screen-height"></span>

<h2>Appcache events</h2>
<pre id="appcache-events">
</pre>
''')

        self.add('</div>')

    #----------------------------------------------------------------
    def pageMenu(self):
        self.add('')
        self.add('\t<h1>French Quarter Festival 2011</h1>')
        self.add('\t<div class="menu">')
        self.add('\t\t<span class="button button-events">events</span>')
        self.add('\t\t<span class="button button-bands">bands</span>')
        self.add('\t\t<span class="button button-venues">venues</span>')
        self.add('\t\t<span class="button button-map">map</span>')
        self.add('\t\t<span class="button button-tools">+</span>')
        self.add('\t</div>')
        
    #----------------------------------------------------------------
    def filterMenu(self):
        self.add('')
        self.add('\t<div class="menu">')
        self.add('\t\t<span class="toggle button-day-Thu">thu</span>')
        self.add('\t\t<span class="toggle button-day-Fri">fri</span>')
        self.add('\t\t<span class="toggle button-day-Sat">sat</span>')
        self.add('\t\t<span class="toggle button-day-Sun">sun</span>')
        self.add('\t\t<span class="toggle button-fav">&#x2605;</span>')
        self.add('\t</div>')
        
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
    timePattern = re.compile(r"(\d+):(\d+)")

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
        self.timeSampm = timeSampm.lower()
        self.timeE     = timeE
        self.timeEampm = timeEampm.lower()
        self.band      = band
        self.id        = re.sub(r"[^\w]", "-", "fav-%s %s %s" % (band, date, timeS))
        
        yy = int(date[0:4])
        mm = int(date[5:7])
        dd = int(date[8:10])
        
        match = Event.timePattern.match(timeS)
        if not match:
            error("invalid time for %s: %s" % (band, timeS))
            
        try:
            hhh = int(match.group(1))
            mmm = int(match.group(2))
        except:
            error("invalid time for %s: %s:%s" % (band, match.group(1), match.group(2)))
        
        if (self.timeSampm == "pm") and (hhh != 12):
            hhh += 12
            
        self.timeCmp = hhh * 60 + mmm
        
        self.day = datetime.date(yy, mm, dd).strftime("%a")
        
        Event.events.append(self)
    

#--------------------------------------------------------------------
def compareEventsByTime(e1, e2):
    result = cmp(e1.date, e2.date)
    if result: return result
    
    result = cmp(e1.timeCmp, e2.timeCmp)
    if result: return result
    
    return cmp(e1.venue, e2.venue)

#--------------------------------------------------------------------
def compareEventsByBand(e1, e2):
    result = cmp(e1.band, e2.band)
    if result: return result

    result = cmp(e1.date, e2.date)
    if result: return result
    
    return cmp(e1.timeCmp, e2.timeCmp)

#--------------------------------------------------------------------
def compareEventsByVenue(e1, e2):
    result = cmp(e1.venue, e2.venue)
    if result: return result
    
    result = cmp(e1.date, e2.date)
    if result: return result
    
    return cmp(e1.timeCmp, e2.timeCmp)

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

    patternParts = re.compile(r".*^events:$(.*)^venues:$(.*)", re.MULTILINE | re.DOTALL)
    match = patternParts.match(input)
    
    if not match: error("basic structure wrong for file")

    eventData = match.group(1)
    venueData = match.group(2)
    
    parseEventData(eventData)
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
        if None == venue: 
            log("ERROR: event with unknown venue: %s" % event.venue)
            errors = True
            
    if errors:
        error("stopping because of errors")

#--------------------------------------------------------------------
def bandToId(band):
    return band

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
<!--
<meta name="viewport" content="initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no, width=device-width">
-->
<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0">

<link rel="stylesheet" href="css/mwa-fqf2011.css"/>

<script src="vendor/zepto/zepto.js"></script>
<script src="vendor/underscore/underscore.js"></script>
<script src="vendor/json2/json2.js"></script>
<script src="vendor/modjewel/modjewel-require.js"></script>

<script src="vendor/scooj/scooj.transportd.js"></script>
<script src="modules/common/StackTrace.transportd.js"></script>
<script src="modules/mwa-fqf2011/DB.transportd.js"></script>
<script src="modules/mwa-fqf2011/Main.transportd.js"></script>
<script src="modules/mwa-fqf2011/PageManager.transportd.js"></script>
<script src="modules/mwa-fqf2011/DescManager.transportd.js"></script>
<script src="modules/mwa-fqf2011/FilterManager.transportd.js"></script>
<script src="modules/mwa-fqf2011/Tools.transportd.js"></script>

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