#!/usr/bin/python3
from calendar import Calendar
from datetime import date, datetime, timedelta
from document import Document
from flickity import *
from innerHTML import *
from markdown2 import markdown
import os, json

class HTMLCalendar(DIV):
	""" The <div></div> that contains a training calender month.
	"""
	def build(self, thismonth, thisweek, races):
		self._class = "month"
		sunday = 6
		cal = Calendar(sunday)

		table = TABLE()
		weekdays = TR({"style":"border:0;"})
		weekdays.append(TD("Week"))
		for md in cal.itermonthdates(thismonth.year, thismonth.month):
			weekdays.append('<td class="day">%s</td>' % md.strftime("%a")[:2])
			if md.weekday() == 5: break
		table.append(THEAD(weekdays))

		tbody = TBODY()
		tr = TR()
		currentWeek = False
		for md in cal.itermonthdates(thismonth.year, thismonth.month):
			active = False
			if md.month == thismonth.month: active = True

			if md.weekday() == sunday:
				weeknum = self.getWeekNumber(md, races[0]["racedate"])
				currentWeek = False
				if md == thisweek: currentWeek = True

			td = TD({"class":"day","style":""})
			td.innerHTML = str(md.day)
			if self.isRaceDate(md, races):
				td.style = 'background-color:#cef6c4;font-weight:bold;'
			if active and weeknum > 0:
				td._id = "c%s" % md.strftime("%Y%m%d")
				td.onclick = "javascript:cellClick(%d,'%s');" % (weeknum, md.strftime('%a').lower())
				if currentWeek:
					td.onclick = "javascript:flick('%s');" % md.strftime("%a").lower()
					td.style = "background-color:aliceblue;"
			else:
				if md != races[0]["racedate"]:
					td.style = "color:#dddddd;"
			tr.append(td)
			if md.weekday() == 5:
				td = TD({"class":"week"})
				if weeknum > 0:
					td.innerHTML = str(weeknum)
					td.onclick = "javascript:cellClick(%d,'');" % weeknum
				tr.prepend(td)
				tbody.append(tr)
				tr = TR()
	
		table.append(tbody)
		tablewrap = DIV()
		tablewrap.append(table)
		self.append('<h4>%s</h4>' % thismonth.strftime('%B %Y'))
		self.append(table)
		return
	
	def isRaceDate(self, md, races):
		for race in races:
			if race["racedate"] == md: return True
		return False

	def getWeekNumber(self, md, weekdate):
		delta = timedelta(days=7)
		weeknum = 0
		while(weekdate > md):
			weeknum = (weeknum + 1)
			weekdate = (weekdate - delta)
		return weeknum


class CalendarDocument(Document):
	""" A Flickity web page displays all the months of a training cycle.
	"""
	def handleMarkdown(self, txt, races):
		self.title = "2025 Training Calendar"
		self.description = "My training calendar from December 2024 through October 2025"

		self.masthead = Masthead()
		self.navigation = Navigation()
		self.carousel = Carousel()
		self.pagefooter = PageFooter()
		self.javascript = FlickityJS()
		self.socialIcons = SocialIcons()

		self.head.append(META({"http_equiv":"Content-Type","content":"text/html;charset=utf-8"}))
		self.head.append(META({"http_equiv":"Pragma","content":"no-cache"}))
		self.head.append(META({"http_equiv":"Expires","content":"-1"}))
		self.head.append(META({"name":"viewport","content":"width=device-width,initial-scale=1,user-scalable=no"}))
		self.head.append(META({"name":"author","content":"Mario Stocco"}))
		self.head.append(META({"name":"copyright","content":"2024 Mario Stocco"}))
		self.head.append(META({'name':'description','content':self.description}))
		self.head.append(META({'name':'generator','content':'An iPad Pro and a bit of Python'}))
		self.head.append(LINK({'rel':'stylesheet','type':'text/css','media':'screen','href':'/assets/css/flickity.min.css'}))
		self.head.append(LINK({'rel':'stylesheet','type':'text/css','media':'screen','href':'/assets/css/mstocco.css'}))
		self.head.append(SCRIPT({"src":"/assets/js/flickity.pkgd.min.js"}))
		self.head.append(SCRIPT({"src":"/assets/js/trainingcalendar.js"}))

		self.body.onload = "javascript:fetchActiveDays(fullcalendar);"
		style = STYLE()
		style.append('.cal {width:265px;margin:0 0 0 10px;} ')
		style.append('.cal .month div {height:160px;} ')
		style.append('.cal .month h4 {margin:0;} ')
		style.append('.cal .month div table {font-size:0.8em;border-collapse:collapse;margin-top:-5px;} ')
		style.append('.cal .month .day {text-align:right;width:25px;} ')
		style.append('.cal .month .week {text-align:center;width:35px;}')
		#self.head.append(style)

		firstCell = SECTION({'class':'carousel-cell text','style':'width:300px;'})
		firstCell.append(self.navigation)
		firstCell.append(self.socialIcons)
		self.carousel.append(firstCell)

		textcell = CarouselText(txt)
		textcell._class = "carousel-cell cal"
		textcell.style = "width:265px;"
		self.carousel.append(textcell)
		
		lastrace = date(2025,10,19)
		months = []
		months.append( ((2024,12),(2025,4),(2025,8)))
		months.append( ((2025,1), (2025,5),(2025,9)))
		months.append( ((2025,2), (2025,6),(2025,10)))
		months.append( ((2025,3), (2025,7),(2025,11)))
		for c in range(len(months)):
			cell = DIV({"class":"carousel-cell cal", "style":"width:265px;padding-left:10px;"})
			#cell.append('<div style="height:10px;"></div>')
			for yyyy, mm in months[c]:
				cal = HTMLCalendar({"class":"month"})
				cal.build(date(yyyy,mm,1), lastrace, races)
				cell.append(cal)
			self.carousel.append(cell)
		self.carousel.append(CarouselLast())
		
		horizon = DIV({"class":"horizon"})
		content = DIV({"class":"content"})
		content.append(self.masthead)
		content.append(self.carousel)
		content.append(self.pagefooter)
		horizon.append(content)
		self.body.append(horizon)
		self.body.append(self.javascript)
		return

mdown = """

# TRIATHLON CALENDAR - 2025

Calendar days in: <strong id="tdc">&mdash;</strong>  
Active days: <strong id="adc">&mdash;</strong> &nbsp; <small id="adp" style="padding:2px 2px 2px 10px;background-color:#ddf3ff;">0%</small>

#### Next Race
To be determined...

## ANNUAL GOAL
No IRONMAN races on the calendar this year; if _"they"_ were
to run IM Canada - Penticton this year, _"they"_ would have
already had my money.

Queue up XTERRA Victoria this summer and the 2025 Age-Group
World Champs in Wollongong, Australia in the (our) fall.

Let's go.

## PERIODIC SUMMARY
&mdash;

"""

def decodeRaceDate(empDict):
	if "racedate" in empDict:
		#empDict["racedate"] = dateutil.parser.parse(empDict["racedate"])
		empDict["racedate"] = datetime.strptime(empDict["racedate"], '%Y-%m-%d').date()
	return empDict

if __name__ == "__main__":

	racefile = os.popen('cat ../docs/assets/racedates-2025.json', 'r')
	races = json.load(racefile, object_hook=decodeRaceDate)['races']

	calendar = CalendarDocument('mariostoc.co', '/training', 'calendar-2025')
	calendar.handleMarkdown(mdown, races)
	calendar.save('../docs')
	print('done.')

