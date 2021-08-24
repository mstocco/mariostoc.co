#!/usr/bin/python3
from templateDocument import TemplateDocument
from templateHTML import *
from innerHTML import *
from datetime import date, timedelta
from calendar import Calendar


class CalendarMonth(DIV):
	""" An HTML calendar that highlights where I am at
	    in the build toward Ironman Canada.
	"""
	def __init__(self, yyyy, mm):

		specialDates = []
		specialDates.append(date(2021,9,26))    # Ironman Canada
		specialDates.append(date(2020,10,31))   # 5K Workout
		specialDates.append(date(2020,11,21))   # 5K Workout
		specialDates.append(date(2020,12,5))    # 5KM TT
		specialDates.append(date(2021,6,28))    # Penticton
		specialDates.append(date(2021,6,29))    # Penticton
		specialDates.append(date(2021,6,30))    # Penticton
		specialDates.append(date(2021,7,1))     # Penticton
		specialDates.append(date(2021,7,18))    # Victoria Half

		imc = specialDates[0]	# IronMan Canada
		dateobj = date(yyyy, mm, 1)
		h4 = H4({'style':'margin:0;'})
		h4.innerHTML = dateobj.strftime('%B %Y')
		self.innerHTML = h4.tohtml()
	
		thead = THEAD()
		tr = TR()
		style = 'text-align:left;'
		for h in ['Week','Su','Mo','Tu','We','Th','Fr','Sa']:
			td = TD({'style':style})
			td.innerHTML = h
			tr.append(td)
			style = 'text-align:right;'
		thead.append(tr)

		tbody = TBODY()
		tr = TR()
		daynum = 0
		calObj = Calendar(6)	# Sunday being the first day of the week
		for calDate in calObj.itermonthdates(yyyy, mm):
			td = TD()
			style = {'style':'text-align:right;padding:0 2px;margin:0;width:25px;'}
			if calDate.month != mm:
				style['style'] = '%s;color:#ddd;' % style['style']
			else:
				if calDate <= date.today() or calDate == imc:
					style['style'] = '%s;background-color:greenyellow;' % style['style']
				if calDate in specialDates:
					style['style'] = '%s;font-weight:bold;text-decoration:underline;font-size:1.17em' % style['style']

			td.style = style['style']
			td.innerHTML = str(calDate.day)
			if daynum % 7 == 0:
				wtg = imc - calDate
				if daynum > 0:
					tbody.append(tr)
				weeknum = int(wtg.days / 7)
				href = 'ironman2021-%dweeksout' % weeknum

				wk = TD({'style':'text-align:center;padding:0 2px;margin:0;width:35px;'})
				wk.append(str(weeknum))
				if weeknum < 2:
					wk.innerHTML = 'RACE'
					href = 'ironman2021-raceweek'
					if weeknum < 1:
						wk.innerHTML = '-'
				if calDate <= date.today():
					wk.onclick = 'window.location.assign(\'%s\');' % href

				tr = TR()
				tr.append(wk)

			if calDate <= date.today():
				if calDate in specialDates:
					qstr = calDate.strftime('%a').lower()
					href = '%s?%s' % (href, qstr)
				td.onclick = 'window.location.assign(\'%s\');' % href

			tr.append(td)
			daynum = (daynum + 1)
		tbody.append(tr)
		
		table = TABLE({'style':'font-size:0.8em;border-collapse:collapse;margin-top:-5px;'})
		table.append(thead)
		table.append(tbody)
		div = DIV({'style':'height:162px;'})
		if yyyy == 2020:
			div.style = 'height:142px;border-bottom:1px solid #ddd;'
		div.append(table)
		self.append(div)
		#print(self.tohtml())
		#raise SystemExit


class CalendarMonths(DIV):
	""" Carousel Cell that provides vertical alignment
	    to the tile and calendars.
	"""
	def __init__(self):
		self._class = 'carousel-cell text'
		self.style = 'width:265px;'
		self.innerHTML = ''


class IronmanCalendar(TemplateDocument):
	""" A html representation of my 12 month lead up
	    to Ironman Canada - Penticton.  Eash calendar
		is an HTML table and when rendered, will highlight
		days completed and any special days that I want to
		make note of.  Clicking a week takes you to that
		training log webpage.
	"""
	def template(self):
		self.version = date.today().isoformat()
		self.domain = 'mariostoc.co'
		self.documentURI = '/traininglog/calendar'
		self.description = 'Training Calendar - Ironman 2021'
		self.lastModified = 20210611
		self.masthead = Masthead()
		self.navigation = Navigation()
		self.carousel = Carousel()
		self.pagefooter = PageFooter()
		self.javascript = FlickityJS()
		self.socialIcons = SocialIcons()
		self.opengraph = OpenGraph()

		firstCell = SECTION({'class':'carousel-cell text','style':'width:300px;'})
		firstCell.append(self.navigation)
		firstCell.append(self.socialIcons)
		self.carousel.append(firstCell)
	
		carouselCells = []
		carouselCells.append(CalendarMonths())
		carouselCells.append(CalendarMonths())
		carouselCells.append(CalendarMonths())
		carouselCells.append(CalendarMonths())
		carouselCells.append(CalendarMonths())
		
		div = DIV({'style':'height:32px;'})
		carouselCells[3].append(div)
		carouselCells[2].append(div)
		carouselCells[1].append(div)
		div.innerHTML = H1('IRONMAN TRAINING 2021').tohtml()
		carouselCells[0].append(div)

		mm = 9
		yyyy = 2020
		for r in range(3):
			carouselCells[0].append(CalendarMonth(yyyy, mm))
			carouselCells[1].append(CalendarMonth(yyyy, (mm + 1)))
			carouselCells[2].append(CalendarMonth(yyyy, (mm + 2)))
			carouselCells[3].append(CalendarMonth(yyyy, (mm + 3)))
			mm = (mm + 4)
			if mm > 12:
				mm = 1
				yyyy = 2021

		addendum = P({'style':'font-size:0.8em;background-color:#E0ECF8;padding:0 7px;margin-bottom:32px;'})
		addendum.append('Based on the guidelines from the Province of British Columbia in relation to the COVID-19 pandemic, the 2021 Subaru IRONMAN Canada – Penticton event was postponed from August 29 to September 26')
		
		addendum2 = P({'style':'font-size:0.8em;background-color:#F8C471;padding:0 7px;margin-bottom:28px;'})
		addendum2.append('Unfortunately, due to the updated British Columbia Interior Health restrictions for events hosting more than 100 people, we regret to inform you that the 2021 IRONMAN Canada - Penticton triathlon cannot take place on September 26, 2021.')

		carouselCells[4].append(DIV({'style':'height:28px;'}))
		carouselCells[4].append(H4('CALENDAR UPDATE: June 6, 2021'))
		carouselCells[4].append(addendum)
		carouselCells[4].append(H4('CALENDAR UPDATE: August 23, 2021'))
		carouselCells[4].append(addendum2)
		carouselCells[4].append(CalendarMonth(2021, 9))
		for cell in carouselCells:
			self.carousel.append(cell)
		self.carousel.append(CarouselLast())


