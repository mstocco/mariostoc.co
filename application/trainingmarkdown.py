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
		self.filename = "%s-triathlon2024-%dweeksout.md" % (prefix, weeksout)
		if weeksout < 2:
			racecode = '-'.join(lastrace["race"].split(" ")[:2]).lower()
			self.filename = "%s-%s-raceweek.md" % (prefix, racecode)
			if weeksout < 1:
				self.filename = "%s-%s.md" % (prefix, racecode)
	
		## Calendars (appended near the end of the file)
		month1 = HTMLCalendar()
		month2 = HTMLCalendar()
		if thisdate.month == 10:
			month1.build(thisdate, thisdate, races)
			month2.build((thisdate + timedelta(days=31)), thisdate, races)

		elif thisdate.month == 9:
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
		
		## Weekly Summary
		if weeksout == 1:
			lines = ["# %s RACEWEEK %d" % (thisrace["race"].upper(), thisrace["racedate"].year)]
		else:
			lines = ["# %s TRAINING %d" % (thisrace["race"], lastrace["racedate"].year)]
		lines.append("Week begining [%s %d, %d](javascript:flick('sun');)\n" % (thisdate.strftime("%A, %B"), thisdate.day, thisdate.year))
		
		upnext = []
		daysout = (nextrace["racedate"] - thisdate).days
		if daysout < 22:
			if daysout == 1:
				upnext.append("%s tomorrow" % thisrace["race"])
			else:
				upnext.append("**%d days** until %s" % (daysout, nextrace["race"]))
		else:
			nextweeks = math.ceil((nextrace["racedate"] - thisdate).days / 7)
			upnext.append("%d weeks until %s" % (nextweeks, nextrace["race"]))
		if thisrace["racedate"] < lastrace["racedate"]:
			weeksout = math.ceil((lastrace["racedate"] - thisdate).days / 7)
			lines[-1] = "%s  " % lines[-1]
			upnext.append("%d weeks until %s" % (weeksout, lastrace["race"]))

		lines.append("%s\n" % "<br />".join(upnext))	
		lines.append("### WEEKLY GOAL")
		lines.append("&mdash;\n")
		lines.append("### SUMMARY")
		lines.append("Total Training Time: **0.0&#8239;hours**\n")
		lines.append("I feel like I was... <!--LAGGING  MAINTAINING  BUILDING  PEAKING  OVERREACHING-->\n")
		lines.append("&mdash;\n")
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
				lines.append("Weather: &mdash;°C\n")
				lines.append("### PLANNED WORKOUT")
				lines.append("&mdash;\n")
				lines.append("### NOTES")
				lines.append("Time: **0.0&#8239;hrs** &nbsp; Distance: **0.0&#8239;km**")
				lines.append("\n&mdash;\n")
				lines.append("### NUTRITION")
				lines.append("&mdash;\n\n\n")
			lines.append("<!---->")
			thisdate = (thisdate + delta)
		
		lines.append(month1.tohtml())
		lines.append(month2.tohtml())
		lines.append("\n---\n")
		lines.append("#### MISCELLANEOUS STUFF")
		lines.append('&mdash;\n\n')

		print(self.filename)
		fileobj = open('../content/training/%s' % self.filename, 'w', encoding="utf-8")
		fileobj.write('\n'.join(lines))
		fileobj.close()

		return
		print("\n".join(lines))


def main():
	racefile = os.popen('cat ../docs/assets/racedates.json', 'r')
	races = json.load(racefile, object_hook=decodeRaceDate)['races']
	lastrace = races[0]
	nextrace = races[0]
	thisrace = races[0]
	thisdate = races[0]["racedate"]
	delta = timedelta(days=1)

	stopdate = date(2023,10,1)
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

		if thisdate.weekday() == 6:
			md = MarkdownFile(thisdate, thisrace, nextrace, races)
		thisdate = (thisdate - delta)
		if thisdate < stopdate: break
	return  

main()

