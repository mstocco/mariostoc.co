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


		triathlons = []
		keydates = []
		offdays = []
		
		triathlons.append(date(2023,6,25))    # Challenge Roth
		triathlons.append(date(2023,5,28))    # Victoria 70.3

		keydates.append(date(2023,4,23))	# TC10K
		keydates.append(date(2023,5,21))	# Marriage

		offdays.append(date(2023,1,20))		# COVID
		offdays.append(date(2023,1,21))		# COVID
		offdays.append(date(2023,1,22))		# COVID
		offdays.append(date(2023,1,23))		# COVID
		offdays.append(date(2023,1,24))		# COVID
		offdays.append(date(2023,1,25))		# COVID

		offdays.append(date(2023,3,24))		# Broke Foot
		offdays.append(date(2023,3,25))		# Broke Foot
		offdays.append(date(2023,3,26))		# Broke Foot
		offdays.append(date(2023,3,27))		# Broke Foot
		offdays.append(date(2023,3,28))		# Broke Foot
		offdays.append(date(2023,3,29))		# Broke Foot

		goalrace = triathlons[0]
		imitaly = date(2021,9,18)
		trainingStart = date(2022,10,2)

		dateobj = date(yyyy, mm, 1)

		self.innerHTML = H4(dateobj.strftime('%B %Y')).tohtml()
	
		table = TABLE()
		thead = THEAD()
		tbody = TBODY()

		tr = TR()
		tr.append(TD('Week'))
		for h in ['Su','Mo','Tu','We','Th','Fr','Sa']:
			td = TD({'class':'day'})
			td.innerHTML = h
			tr.append(td)
		thead.append(tr)

		tr = TR()
		daynum = 0
		calObj = Calendar(6)	# Sunday being the first day of the week
		for calDate in calObj.itermonthdates(yyyy, mm):
			td = TD({'class':'day'})
			style = {'style':'text-align:right;padding:0 2px;margin:0;width:25px;'}
			if calDate.month != mm:
				td.style = 'color:#ddd;'
				style['style'] = '%scolor:#ddd;' % style['style']
			elif calDate.month == 9:
				if calDate == imitaly:
					style['style'] = '%sfont-weight:bold;text-decoration:underline;font-size:1.17em;background-color:#33B8FF;' % style['style']
				else:
					td.style = 'color:#ddd;'
					style['style'] = '%scolor:#ddd;' % style['style']
			else:
				if calDate <= date.today():
					if calDate < trainingStart:
						td.style = 'color:#ddd;'
						style['style'] = '%scolor:#ddd;' % style['style']
					elif calDate > date(2021,11,13) and calDate < date(2021,12,19):
						td.style = 'color:orange;'
						style['style'] = '%scolor:orange;' % style['style']
					else:
						td.style = 'background-color:greenyellow;'
						style['style'] = '%sbackground-color:greenyellow;' % style['style']
				if calDate in triathlons:
					td.style = 'font-weight:bold;text-decoration:underline;font-size:1.17em;background-color:#33B8FF;'
				elif calDate in keydates:
					td.style = 'font-weight:bold;text-decoration:underline;font-size:1.17em;background-color:#BCE8FF;'
					style['style'] = '%sfont-weight:bold;text-decoration:underline;font-size:1.17em;background-color:#BCE8FF;' % style['style']
				elif calDate in offdays:
					td.style = 'text-decoration:line-through;background-color:#FFFF66;'

			#td.style = style['style']
			td.innerHTML = str(calDate.day)
			if daynum % 7 == 0:
				wtg = goalrace - calDate
				if daynum > 0:
					tbody.append(tr)
				weeknum = int(wtg.days / 7)
				#href = 'ironman2022-%dweeksout' % weeknum
				href = 'challenge2023-%dweeksout' % weeknum

				wk = TD({'style':'text-align:center;width:35px;'})
				if weeknum < 47:
					wk.append(str(weeknum))
					if weeknum < 2:
						wk.innerHTML = 'RACE'
						#href = 'ironman2022-raceweek'
						href = 'challenge2023-raceweek'
						if weeknum < 1:
							wk.innerHTML = '-'
					if calDate <= date.today():
						wk.onclick = 'window.location.assign(\'%s\');' % href
				else:
					wk.append('-')

				tr = TR()
				tr.append(wk)

			if calDate <= date.today():
				if calDate in triathlons:
					qstr = calDate.strftime('%a').lower()
					href = '%s?%s' % (href, qstr)
				elif calDate == imitaly:
					href = '/racereports/2021-ironman-italy-emilia-romagna'
				td.onclick = 'window.location.assign(\'%s\');' % href

			tr.append(td)
			daynum = (daynum + 1)
		tbody.append(tr)
		
		table.append(thead)
		table.append(tbody)
		div = DIV({'style':'height:162px;'})
		if yyyy == 2022:
			div.style = 'height:152px;border-bottom:1px solid #ddd;'
		div.append(table)
		self.append(div)
		self._class = 'month'


class CalendarMonths(DIV):
	""" Carousel Cell that provides vertical alignment
	    to the tile and calendars.
	"""
	def __init__(self):
		self._class = 'carousel-cell cal'
		self.style = 'width:265px;'
		self.innerHTML = ''


class IronmanCalendar(TemplateDocument):
	""" A html representation of my lead up to my next
	    goal race. Each calendar is an HTML table and when
		rendered, will highlight days completed and any 
		special days that I want to make note of.  Clicking
		a week takes you to that training log webpage.
	"""
	def template(self):
		self.version = date.today().isoformat()
		self.domain = 'mariostoc.co'
		self.title = 'Training Calendar 2023'
		self.documentURI = '/traininglog/calendar'
		self.description = 'Training Calendar - Challenge Roth 2023'
		self.lastModified = 20220905
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
		
		div = DIV({'style':'height:32px;'})
		#carouselCells[3].append(div)
		carouselCells[2].append(div)
		carouselCells[1].append(div)
		div.innerHTML = H2('CHALLENGE ROTH TRAINING - 2023').tohtml()
		carouselCells[0].append(div)

		mm = 10
		yyyy = 2022
		for r in range(3):
			carouselCells[0].append(CalendarMonth(yyyy, mm))
			carouselCells[1].append(CalendarMonth(yyyy, (mm + 1)))
			carouselCells[2].append(CalendarMonth(yyyy, (mm + 2)))
			#carouselCells[3].append(CalendarMonth(yyyy, (mm + 3)))
			mm = (mm + 3)
			if mm > 12:
				mm = 1
				yyyy = 2023

		for cell in carouselCells:
			self.carousel.append(cell)

		self.carousel.append(CarouselImage('![](/assets/jpg/IMG_1336-549x550.jpeg)'))
		self.carousel.append(CarouselLast())

		style = STYLE()
		style.append(' .cal {width:265px;margin:0 0 0 10px;} ')
		style.append(' .cal .month div {height:152px;} ')
		style.append(' .cal .month h4 {margin:0;} ')
		style.append(' .cal .month div table {font-size:0.8em;border-collapse:collapse;margin-top:-5px;} ')
		style.append(' .cal .month .day {text-align:right;width:25px;} ')

		self.head.append(style)
