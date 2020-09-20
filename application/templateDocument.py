#!/usr/bin/python3
from innerHTML import *
from templateHTML import *
import hashlib


class TemplateDocument(HTML5Document):
	""" This is how my webage gets built.
	"""
	def template(self):
		self.domain = 'mariostoc.co'
		self.documentURI = '/'
		self.description = ''
		self.lastModified = 20200814
		self.masthead = Masthead()
		self.navigation = Navigation()
		self.carousel = Carousel()
		self.pagefooter = PageFooter()
		self.javascript = FlickityJS()
		self.socialIcons = SocialIcons()
		self.opengraph = OpenGraph()

	def handleMarkdown(self, contentPath):		
		""" 
		"""
		with open(contentPath, 'r', encoding='utf-8') as fileobj:
			content = fileobj.read().strip()
		for line in content.split('\n'):
			if len(line) > 1 and line[0] == '#':
				self.title = line.replace('#', '').strip()
				self.opengraph.title = self.title
				break
		lines = []
		for line in content.split('\n'):
			if getattr(self, 'title', None):
				if line.find('<!---->') == 0:
					section = CarouselText('\n'.join(lines))
					if contentPath.find('traininglog') > 1:
						for day in ['MON','TUE','WED','THU','FRI','SAT']:
							if section.innerHTML.find('<h2>%s' % day) == 0:
								section.style = 'border-left:1px solid #ddd;'
					self.carousel.append(section)
					lines = []
				elif line.find('![') == 0 and line.find('x550') > 1:
					if len(lines) > 0:
						self.carousel.append(CarouselText('\n'.join(lines)))
					self.carousel.append(CarouselImage(line))
					lines = []
				else:
					if line.find('<!--') == 0 and line.find(': ') > 5:
						if line.find('<!--og:') == 0:
							property = line[7:].split(': ')[0]
							content = line.split(': ')[1].split('-->')[0]
							self.opengraph.append(property, content)
							continue
						if line.find('<!--description') == 0:
							self.description = line.split(': ')[1].split('-->')[0].strip()
							if not hasattr(self.opengraph, 'description'):
								self.opengraph.append('description', self.description)
							continue
					lines.append(line)
			else:
				if line.find('![') == 0 and line.find('x550') > 1:
					carouselimg = CarouselImage(line)
					if hasattr(carouselimg, 'title'):
						self.title = carouselimg.title
						self.opengraph.title = self.title
					self.carousel.append(carouselimg)
				else:
					self.title = line.replace('#', '').strip()
					lines.append(line)
		if len(lines) > 0:
			section = CarouselText('\n'.join(lines))
			if contentPath.find('traininglog') > 1:
				if section.innerHTML.find('<h2>SAT') == 0:
					section.style = 'border-left:1px solid #ddd;'
			self.carousel.append(section)
		firstCell = SECTION({'class':'carousel-cell text','style':'width:300px;'})
		firstCell.append(self.navigation)
		firstCell.append(self.socialIcons)
		self.carousel.prepend(firstCell)
		self.carousel.append(CarouselLast())
		self.version = self.getSHA1(content.encode('utf-8'))
	
	def getSHA1(self, content):
		hash = hashlib.new('sha1')
		hash.update(content)
		return hash.hexdigest()[:7]
		
	def tohtml(self):
		meta = []
		meta.append({"http_equiv":"Content-Type","content":"text/html;charset=utf-8"})
		meta.append({"name":"viewport","content":"width=device-width,initial-scale=1,user-scalable=no"})
		meta.append({"name":"x-version","content":self.version})
		meta.append({'name':'Description','content':self.description})
		meta.append({"name":"Author","content":"Mario Stocco"})
		meta.append({"name":"Copyright","content":"Mario Stocco"})
		meta.append({"name":"Generator","content":"Mario Stocco"})
		for attrs in meta:
			self.head.append(META(attrs))
		self.opengraph.url = 'https://mariostoc.co%s' % self.documentURI
		self.head.append(self.opengraph)
		attrs = {'rel':'stylesheet','type':'text/css','media':'screen'}
		for href in ['webtype_fonts.min.css','flickity.min.css','mstocco.css?v=004']:
			attrs['href'] = '/assets/css/%s' % href
			self.head.append(LINK(attrs))
		
		self.head.append(SCRIPT({"src":"/assets/js/flickity.pkgd.min.js"}))
		if self.documentURI.find('/pictures/') == 0:
			self.javascript.flkty['initialIndex'] = 2

		content = DIV({"class":"content"})
		content.append(self.masthead)
		content.append(self.carousel)
		content.append(self.pagefooter)

		horizon = DIV({"class":"horizon"})
		horizon.append(content)
		self.body.append(horizon)
		self.body.append(self.javascript)
		return HTML5Document.tohtml(self)


class RedirectDocument(HTML5Document):
	def template(self):
		self.documentURI = '/'
		self.title = 'Mario Stocco'
		self.url = 'https://mariostoc.co/'

	def tohtml(self):
		anchor = A({"href":self.url})
		anchor.innerHTML = " %s" % self.url
		forward = P('This page is trying to send you to ')
		forward.append(anchor)

		anchor = A({'href':'#','onclick':'history.back();'})
		anchor.innerHTML = 'return to the previous page.'
		backward = P('If you do not want to visit that page, you can ')
		backward.append(anchor)

		self.head.append(META({"http-equiv":"refresh","content":".2;url=%s" % self.url}))
		self.head.append(TITLE(self.title))
		self.head.append(LINK({'rel':'stylesheet','type':'text/css','media':'screen','href':'/assets/css/webtype_fonts.min.css'}))
		self.head.append(LINK({'rel':'stylesheet','type':'text/css','media':'screen','href':'/assets/css/mstocco.css'}))
		self.body.append(H2('REDIRECT NOTICE'))
		self.body.append(forward)
		self.body.append(backward)
		self.body._class = "text"
		self.body.style = "font-size:0.8em;"
		self.documentElement.append(self.head)
		self.documentElement.append(self.body)
		return '%s%s' % (self.doctype, self.documentElement.tohtml())

