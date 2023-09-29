#!/usr/bin/python3
## ________________________________________________
## Templated Document/HTML5 Tag Definitions
##
## All the little bits to put together the Flickity 
## themed website.
from document import Document
from markdown2 import markdown
from innerHTML import *


class Masthead(HEADER):
	""" Seen above the Flickity Carousel.
	    This toogles the site navigation and provides a
	    link to the home page.
	"""
	def __init__(self):
		self._class = 'masthead'
		self.innerHTML = ''
		path = PATH({"d":"M0,16.666H20V14.444H0ZM0,11.111H20V8.888H0ZM0,3.333V5.5555H20V3.333Z"})
		svg = SVG({"focusable":"false","viewbox":"0 0 20 20"})
		div = DIV({"class":"icon","role":"button","onclick":"javascript:toggle();"})
		anchor = A({"href":"/","class":"mariostocco"})
		anchor.innerHTML = 'MARIO STOCCO'
		svg.append(path)
		div.append(svg)
		self.append(div)
		self.append(anchor)


class Carousel(MAIN):
	""" This is responsible for the horizontally swipeable
	    layout of the site.  The HTML behind it is based on
	    Flickity (https://github.com/metafizzy/flickity).
	"""
	def __init__(self):
		self._id = 'carousel'
		self._class = 'carousel'
		self.width = 300
		self.innerHTML = ''

	def append(self, section):
		if hasattr(section, 'width'):
			self.width = (self.width + section.width)
			del section.width
		HTML5Tag.append(self, section)
		return

	def tohtml(self):
		del self.width
		return HTML5Tag.tohtml(self)


class CarouselText(DIV):
	""" Unlike other HTML5Tag definitions, this class processes
	    text with the markdown2.markdown module to generate the
	    innerHTML attribute.
	"""
	def __init__(self, text):
		self._class = 'carousel-cell text'
		if text.find('```') == -1:
			lines = []
			for line in markdown(text).split('\n'):
				lines.append(line.strip() + ' ')
			self.innerHTML = ''.join(lines)
		else:
			self.innerHTML = markdown(text)


class CarouselImage(DIV):
	""" Unlike other HTML5Tag definitions, this class processes
	    the markdown reference to an image.  Instead of creating 
	    an IMG tag, this website displays the image as the 
	    background image contains within the _x550 dimensions of
	    a carousel cell.
	"""
	def __init__(self, text):
		""" ![alt text](url "title") """
		self._class = 'carousel-cell image'
		self.innerHTML = ''
		text = text.strip()
		alttext = text[2:].split(']')[0].strip()
		url = text.split('(')[1].split(')')[0].split(' ')[0]
		title = text.split(url)[1].split(')')[0].strip()
		if len(title) > 0:
			self.title = title
		try:
			filename = url.split('/')[-1]
			if filename.find('-'):
				self.width = int(filename.split('-')[-1].split('x')[0])
			else:
				self.width = int(filename.split('x')[0])
		except:
			self.width = 340
	
		style = []
		style.append('width:%dpx' % self.width)
		style.append('background-image:url(%s)' % url)
		self.style = ';'.join(style)
		
		banner = DIV({'class':'banner'})
		div_height = 0
		div_width = (self.width - 20)
		if len(title) > 0:
			banner.append(H3(title))
			div_height = (div_height + 20)
		if len(alttext) > 0:
			banner.append(P(alttext))
			div_height = (div_height + 20)
		if banner.length > 0:
			banner.style = 'height:%dpx;width:%dpx;' % (div_height, div_width)
			imagebanner = DIV({'class':'imagebanner'})
			imagebanner.append(banner)
			self.append(imagebanner)


class CarouselLast(ASIDE):
	""" Unlike other HTML5Tag definitions, this class processes
	    text with the markdown2.markdown module to generate the
	    innerHTML attribute.
	"""
	def __init__(self):
		self._class = 'carousel-cell last'
		self.style = 'width:50%'
		div1 = DIV({"style":"width:95%;margin-top:245px;"})
		div2 = DIV({"onclick":"javascript:toggle();","style":"margin-left:75%","role":"button"})
		svg = IMG({"src":"/assets/img/arrow-left.svg","style":"width:40px;"})	
		div2.append(svg)
		div1.append(div2)
		self.innerHTML = div1.tohtml()


class Navigation(NAV):
	""" This NAV element is nested in the first SECTION of
	    the Carousel.
	"""
	def __init__(self):
		self.links = []
		self.links.append({'href':'/traininglog/', 'label':'TRAINING LOG'})
		self.links.append({'href':'/racereports/', 'label':'RACE REPORTS'})
		self.links.append({'href':'/blog/', 'label':'THINGS I\'VE WRITTEN'})
		self.links.append({'href':'/pictures/', 'label':'PICTURES I\'VE TAKEN'})
		self.links.append({'href':'/about', 'label':'ABOUT ME'})
		input1 = INPUT({"name":"q","id":"q","type":"text","maxlength":"200","placeholder":"search..."})
		input2 = INPUT({"name":"q","type":"hidden","value":"site:mariostoc.co"})
		google = FORM({"action":"https://google.com/search"})
		google.append(input1)
		google.append(input2)
		self.traininglog = False
		self.innerHTML = google.tohtml()

	def traininglogSubmenu(self):
		ul = UL({'class':'alt','style':'font-size:0.75em;margin:15px 0 0 60px;'})

		anchor = A({'href':'/traininglog/calendar'})
		anchor.innerHTML = 'FULL TRAINING CALENDAR'
		li = LI({'class':'item'})
		li.append(anchor)
		ul.append(li)

		if hasattr(self, 'week'):
			for day in ['SUNDAY','MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY']:
				anchor = A({'href':'javascript:flick(\'%s\');' % day[:3].lower()})
				anchor.innerHTML = day
				li = LI({'class':'item'})
				li.append(anchor)
				ul.append(li)

		for optional in ['before','after','lastyear']:
			if hasattr(self, optional):
				option = getattr(self, optional)
				anchor = A({'href': option['href']})
				anchor.innerHTML = option['name']
				li = LI({'class':'item'})
				li.append(anchor)
				ul.append(li)

		return ul.tohtml()

	def tohtml(self):
		ul = UL({"class":"alt"})
		for attrs in self.links:
			anchor = A({'href':attrs['href']})
			anchor.innerHTML = attrs['label']
			li = LI({"class":"item"})
			li.append(anchor)
			if anchor.innerHTML == 'TRAINING LOG':
				if self.traininglog:
					li.append(self.traininglogSubmenu())
			ul.append(li)
		self.append(ul)
		return HTML5Tag.tohtml(self)


class SocialIcon(DIV):
	""" This is this list item element that contains an
		anchor tag that points to an account that I have
		somewhere else on the inter-webs.
	"""
	def __init__(self, alt, href):
		self._id = 'icon-%s' % alt.lower()		
		src = '/assets/img/%s.svg' % alt.lower()
		anchor = A({"href":href,"target":"_blank","rel":"noreferrer"})
		anchor.append(IMG({"src":src,"alt":alt}))
		self.innerHTML = anchor.tohtml()


class SocialIcons(DIV):
	""" There are 5 links to account pages on other sites.
	    They are displayed in this DIV tag which is found
	    at the bottom of the carousel's first cell.
	"""
	def tohtml(self):
		self._class = 'social'
		self.innerHTML = P('SOCIALLY PROFILED').tohtml()
		self.append(SocialIcon('Strava', 'https://www.strava.com/athletes/21702937'))
		self.append(SocialIcon('Garmin', 'https://connect.garmin.com/modern/profile/_canadian'))
		self.append(SocialIcon('Linkedin', 'https://www.linkedin.com/in/voipexpert'))
		self.append(SocialIcon('GitHub', 'https://github.com/mstocco'))
		return HTML5Tag.tohtml(self)


class PageFooter(FOOTER):
	""" Footer for the bottom of the webpage.
	"""
	def tohtml(self):
		copyright = P("Copyright &copy; 2023 Mario Stocco &nbsp; All rights reserved.")
		self.append(copyright)
		return HTML5Tag.tohtml(self)


class FlickityJS(SCRIPT):
	""" Javascript Tag included in the body of the document.
	"""
	def __init__(self):
		self._type = 'text/javascript'
		self.flkty = {}
		self.flkty['initialIndex'] = 1
	
	def tohtml(self):
		self.innerHTML = "var elem=document.getElementById('carousel');"
		self.append("var flkty=new Flickity(elem,{")
		self.append(" prevNextButtons:false,")
		self.append(" cellAlign:'left',")
		self.append(" bgLazyLoad:3,")
		self.append(" accessibility:true,")
		self.append(" contain:1,")
		self.append(" initialIndex:%d," % self.flkty['initialIndex'])
		self.append(" imagesLoaded:true,")
		self.append(" freeScroll:true")
		self.append("});")
		self.append("function toggle(){if(flkty.selectedIndex>0){flkty.select(0);}else{flkty.select(1);}};")
		self.append("function flick(id){for(i=0;i < flkty.cells.length; i++){if(flkty.cells[i]['element']['id'] == id){flkty.select(i);break;};};};")
		self.append("function scroll(){var id=window.location.search.substr(1).split('=')[0];if(id){flick(id);};};")
		return HTML5Tag.tohtml(self)


class OpenGraph:
	""" A collection of metatags that have a set of
	    minimum requirements before being added to the
	    HEAD tag of a Document.
	"""
	def __init__(self):
		self.article = {'author':'https://mariostoc.co/about'}
		self.og_type = 'article'

	def append(self, prop, content):
		value = content.strip()
		if len(value) > 0:
			if prop.find('article') == 0:
				for key in ['author','published_time','modified_time','expiration_time','section']:
					if prop.find(key) > 0:
						self.article[key] = value
						return
			attr = prop.replace(':', '_')
			setattr(self, attr, value)
		return

	def tohtml(self):
		""" The manatory properties required for the document:
			og:title - The title of your object as it should appear in the graph.
			og:type - The type of your object, e.g., "article".
			og:image - An image URL representing your 1200x630 object within the graph.
			og:url - The canonical URL of your object; e.g. "https://www.imdb.com/title/tt0117500/"
		"""
		tags = []
		for key in ['og_title','og_type','og_image','og_url']:
			if key in self.__dict__.keys():
				meta = META({'property':key.replace('_', ':'), 'content':self.__dict__[key]})
				tags.append(meta.tohtml())

		if len(tags) == 4:
			if 'og_description' in self.__dict__.keys():
				tags.append('<meta property="og:description" content="%s" />' % self.og_description)

			if self.og_type == 'article':
				"""	article:published_time - datetime - When the article was first published.
					article:modified_time - datetime - When the article was last changed.
					article:expiration_time - datetime - When the article is out of date after.
					article:author - profile array - Writers of the article.
					article:section - string - A high-level section name. E.g. Technology
				"""
				for key in ['published_time','modified_time','expiration_time','author','section']:
					if key in self.article:
						tags.append(META({'property':'article:%s' % key, 'content':self.article[key]}).tohtml())
			return ''.join(tags)
		return ''


class FlickityDocument(Document):
	def handleMetaData(self, line):
		key = line[1:].split(']')[0].strip()
		value = line.split(']:- ')[1].strip()
		if len(value) > 0:
			if key == 'title':
				self.opengraph.append('og:title', value)
				self.title = value
			elif key == 'description':
				self.head.append(META({'name':key, 'content':value}))
				self.opengraph.append('og:description', value)
			elif key.find('og:') == 0 or key.find('article:') == 0:
				if key.find('og:image') == 0:
					if value.find('.jpeg') > 0: self.opengraph.append('og:image:type', 'image/jpeg')
					if value.find('http:') == 0: value = value.replace('http:', 'https:')
				self.opengraph.append(key, value)
				if not hasattr(self.opengraph, 'og_url'):
					self.opengraph.append('og:url', self.URL)
				if key == 'article:published_time':
					if 'modified_time' not in self.opengraph.article:
						self.opengraph.append('article:modified_time', self.lastModified)

	def appendCarouselText(self, lines):
		if len(lines) > 0:
			div = DIV({'class':'carousel-cell text', 'width':340})
			div.append(self.formatHTML('\n'.join(lines)))
			self.carousel.append(div)
			return True
		return False

	def formatHTML(self, text):
		if text.find('```') > 0:
			return markdown(text)
		lines = []
		for line in markdown(text).split('\n'):
			line = line.strip()
			if len(line) > 1:
				if line[-1] != '>': line = line + ' '
				elif line[-2] == '/': line = line + ' '
			lines.append(line)
		return ''.join(lines)

	def handleMarkdown(self, contentPath):
		## Elements of this flickity themed page
		self.masthead = Masthead()
		self.navigation = Navigation()
		self.carousel = Carousel()
		self.pagefooter = PageFooter()
		self.javascript = FlickityJS()
		self.socialIcons = SocialIcons()
		self.opengraph = OpenGraph()
	
		if self.documentURI.find('training') == 1:
			training = True
			self.body.onload = 'javascript:getActiveDays(weekday);'
			week = self.documentURI.split('-')[1].split('week')[0]
			self.navigation.traininglog = True
			self.navigation.week = True
	
		elif self.documentURI.find('pictures') == 1:
			self.javascript.flkty['initialIndex'] = 2

		with open(contentPath, 'r', encoding='utf-8') as fileobj:
			content = fileobj.readlines()

		lines = []
		for line in content:
			line = line.rstrip('\r\n')
			if line.find('<!----') == 0:
				if self.appendCarouselText(lines): lines = []
				if line.find('<!----->') == 0:
					lines.append('<div style="height:27px;"></div>')
	
			elif line.find('x550') > 0 and line.find('![') == 0:
				if self.appendCarouselText(lines): lines = []
				image = CarouselImage(line)
				if hasattr(image, 'title') and len(self.title) == 0:
					self.title = image.title
				self.carousel.append(image)

			elif line.find(']:- ') > 3 and line[0] == '[':
				self.handleMetaData(line)
			else:
				if len(self.title) == 0 and line.find('# ') == 0:
					self.title = line[2:].strip()
					if not hasattr(self.opengraph, 'og_title'):
						self.opengraph.append('og:title', self.title)
				if contentPath.find('training') == 1:
					for day in ['SUN','MON','TUE','WED','THU','FRI','SAT']:
						if line.find('## %s' % day) == 0:
							div._id = day.lower()
							if day != 'SUN': div.style = 'border-left:2px solid #e6e6e6;padding-left:8px;'
							break
				lines.append(line)
		self.appendCarouselText(lines)

		firstCell = SECTION({'class':'carousel-cell text','style':'width:300px;'})
		firstCell.append(self.navigation)
		firstCell.append(self.socialIcons)
		self.carousel.prepend(firstCell)
		self.carousel.append(CarouselLast())

		self.head.prepend(META({"name":"author","content":"Mario Stocco"}))
		self.head.prepend(META({"name":"generator","content":"Mario Stocco"}))
		self.head.prepend(META({"name":"copyright","content":"© 2023 Mario Stocco"}))
		self.head.prepend(META({"name":"viewport","content":"width=device-width,initial-scale=1,user-scalable=no"}))
		if hasattr(self, 'nocache'):
			self.head.prepend(META({"http_equiv":"Expires","content":"-1"}))
			self.head.prepend(META({"http_equiv":"Pragma","content":"no-cache"}))
		self.head.prepend(META({"http_equiv":"Content-Type","content":"text/html;charset=utf-8"}))

		self.head.append(self.opengraph)
		self.head.append(LINK({'rel':'stylesheet','type':'text/css','media':'screen','href':'/assets/css/flickity.min.css'}))
		self.head.append(LINK({'rel':'stylesheet','type':'text/css','media':'screen','href':'/assets/css/mstocco.css'}))
		self.head.append(SCRIPT({"src":"/assets/js/flickity.pkgd.min.js"}))
	
		horizon = DIV({"class":"horizon"})
		content = DIV({"class":"content"})
		content.append(self.masthead)
		content.append(self.carousel)
		content.append(self.pagefooter)
		horizon.append(content)
		self.body.append(horizon)
		self.body.append(self.javascript)
		return

