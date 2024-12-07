#!/usr/bin/python3

from trainingcalendar import HTMLCalendar
from datetime import timedelta, datetime, date
import os
import json
import math

def decodeRaceDate(empDict):
	if "racedate" in empDict:
		#empDict["racedate"] = dateutil.parser.parse(empDict["racedate"])
		empDict["racedate"] = datetime.strptime(empDict["racedate"], '%Y-%m-%d').date()
	return empDict


class MarkdownFile:
	def __init__(self, thisdate, thisrace, nextrace, races):
		lastrace = races[0]
		prefix = thisdate.strftime("%Y%m%d")
		weeksout = math.ceil((lastrace["racedate"] - thisdate).days / 7)
		
		self.filename = '%s-2025-%d-weeks-out.md' % (prefix, weeksout)
		if weeksout < 2:  self.filename = '%s-2025-race-week.md' % prefix
		if weeksout < 1:  self.filename = '%s-2025-season-end.md' % prefix

		## Calendars (appended near the end of the file)
		##
		month1 = HTMLCalendar()
		month2 = HTMLCalendar()
		if thisdate.month == 12:
			month1.build(thisdate, thisdate, races)
			month2.build((thisdate + timedelta(days=31)), thisdate, races)
		elif thisdate.month == 11:
			month1.build((thisdate - timedelta(days=30)), thisdate, races)
			month2.build(thisdate, thisdate, races)
		else:
			if thisdate.day > 15:
				# This month and next month""
				month1.build(thisdate, thisdate, races)
				month2.build((thisdate + timedelta(days=21)), thisdate, races)
			else:
				# Last month and this month
				month1.build((thisdate - timedelta(days=21)), thisdate, races)
				month2.build(thisdate, thisdate, races)

		## Build some descriptive content
		abdyyyy = '%s %d, %d' % (thisdate.strftime('%A, %B'), thisdate.day, thisdate.year)
		ogdesc = 'My triathlon training week beginning %s.' % abdyyyy
		upnext = []
		daysout = (thisrace["racedate"] - thisdate).days
		title = '%d Training Week %d' % (lastrace['racedate'].year, weeksout)
		if daysout < 22:
			if daysout == 0:
				title = 'Training Log 2025'
				fullday = thisrace['racedate'].strftime('%A')
				upnext.append('%s on [%s](javascript:flick(\'sun\');)' % (thisrace['race'], fullday))
				ogdesc = '%s The %s race is this %s!' % (ogdesc, thisrace['race'], fullday)
			elif daysout == 1:
				upnext.append('%s tomorrow' % thisrace['race'])
				ogdesc = '%s The %s race is tomorrow!' % (ogdesc, thisrace['race'])
			else:
				if daysout < 8:
					title = '%d %s Race Week' % (thisrace['racedate'].year, thisrace['race'])
				upnext.append('**%d days** until %s' % (daysout, nextrace["race"]))
				ogdesc = '%s %d days until %s.' % (ogdesc, daysout, nextrace['race'])
		else:
			nextweeks = math.ceil((nextrace['racedate'] - thisdate).days / 7)
			upnext.append('%d weeks until %s' % (nextweeks, nextrace['race']))
			ogdesc = '%s %d weeks until %s.' % (ogdesc, nextweeks, nextrace['race'])


		## Start building the Markdown, line by line
		lines = []
		lines.append('[title]:- %s - Week %d' % (title, weeksout))
		lines.append('[description]:- Triathlon training week beginning %s' % abdyyyy)
		lines.append('[og:image]:: https://mariostocco/assets/og/training-2025.jpeg')
		lines.append('[og:description]:- %s' % (ogdesc))
		lines.append('[article:published_time]:- 20241208T235959Z')
		lines.append('[article:section]:- 2025 Training')
		lines.append('\n\n')
		
		if weeksout == 1:
			lines.append('# %d %s RACEWEEK' % (thisrace['racedate'].year, thisrace['race'].upper()))
		else:
			lines.append('# %s' % title.upper())
		lines.append("Week beginning [%s](javascript:flick('sun');)\n" % abdyyyy)

		if thisrace["racedate"] < lastrace["racedate"]:
			weeksout = math.ceil((lastrace["racedate"] - thisdate).days / 7)
			lines[-1] = "%s  " % lines[-1]
			upnext.append("%d weeks until %s" % (weeksout, lastrace["race"]))

		lines.append("%s\n" % "<br />".join(upnext))	
		lines.append("### CURRENT FOCUS")
		if thisdate.month == 12:
			lines.append("Redeveloping healthly habits.\n")
		elif thisdate.month in [1,2,3]:
			lines.append("Winter base training.\n")
		else:
			lines.append("&mdash;\n")
		lines.append("### SUMMARY")
		lines.append("Total Training Time: **0.0&#8239;hours**\n")
		lines.append("I feel like I was... <!--LAGGING  MAINTAINING  BUILDING  PEAKING  OVERREACHING-->\n")
		lines.append("&mdash;\n\n\n\n\n")
		lines.append("![](/assets/svg/image-977x550.svg)\n")
		
		## Individual days of this week
		delta = timedelta(days=1)
		for d in range(7):
			if thisdate == thisrace["racedate"]:
				lines.append("## %s %d - RACE DAY\n" % (thisdate.strftime("%A %b").upper(), thisdate.day))
				lines.append("<h3 style=\"margin-top:20px;\">%d %s</h3>" % (thisdate.year, thisrace["race"]))
				lines.append("Weather: &mdash;°C  \nWater Temp: &mdash;°C")
				lines.append("\n\n")
				lines.append("### RACE SUMMARY")
				lines.append("&mdash;\n\n\n")
			else:
				lines.append("## %s %d" % (thisdate.strftime("%A %b").upper(), thisdate.day))
				lines.append("Sleep **-** | Fatigue **-** | Stress **-** | Soreness **-**")
				lines.append("<sup><br />Rate on a scale 1-7 &nbsp; 1=best 7=worst &nbsp; +5 is a warning</sup>\n")
				lines.append("### WORKOUT\n&mdash;\n")
				lines.append("### NOTES\n&mdash;\n\n")
			lines.append("<!---->")
			thisdate = (thisdate + delta)
		
		lines.append("## END OF WEEK NOTES")
		lines.append("&mdash;\n\n\n")
		lines.append('\n\n---\n\n')
		lines.append(month1.tohtml())
		lines.append(month2.tohtml())

		## Save the Markdown
		fileobj = open('../content/training/%s' % self.filename, 'w', encoding="utf-8")
		fileobj.write('\n'.join(lines))
		fileobj.close()
		return


def main():
	racefile = os.popen('cat ../docs/assets/racedates-2025.json', 'r')
	races = json.load(racefile, object_hook=decodeRaceDate)['races']
	lastrace = races[0]
	nextrace = races[0]
	thisrace = races[0]
	thisdate = races[0]["racedate"]
	delta = timedelta(days=1)

	## Count backwards from last race until...
	stopdate = date(2024,12,1)
	for d in range(365):
		raceday = False
		for race in races:
			if race["racedate"] > thisdate:
				if race["racedate"] > nextrace["racedate"]:
					continue
				nextrace = race
			if race["racedate"] == thisdate:
				thisrace = race
				if thisdate.weekday() == 6: break
				nextrace = race
				break

		print(thisdate)
		if thisdate.weekday() == 6:
			md = MarkdownFile(thisdate, thisrace, nextrace, races)
		thisdate = (thisdate - delta)
		if thisdate < stopdate: break
	return  

main()

