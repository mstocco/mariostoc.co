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
	
	def handleMarkdown(self, contentPath):
		self.documentURI = contentPath.split('content')[1]
		filename = self.documentURI.split('/')[-1]
		target = filename.split('.md')[0] 
		if len(target) > 9:
			if target[:8].isnumeric():
				self.lastModified = int(target[:8])
				target = '-'.join(target.split('-')[1:])
		self.documentURI = self.documentURI.replace(filename, target) 

		with open(contentPath, 'r', encoding='utf-8') as fileobj:
			content = fileobj.read().strip()
		
		lines = []
		for line in content.split('\n'):
			if getattr(self, 'title', None):
				if line.find('<!---->') == 0:
					section = CarouselText('\n'.join(lines))
					self.carousel.append(section)
					lines = []
				elif line.find('![') == 0 and line.find('x550') > 1:
					txtSection = CarouselText('\n'.join(lines))
					imgSection = CarouselImage(line)
					self.carousel.append(txtSection)
					self.carousel.append(imgSection)
					lines = []
				else:
					lines.append(line)
			else:
				self.title = line.replace('#', '').strip()
				lines.append(line)
		if len(lines) > 0:
			section = CarouselText('\n'.join(lines))
			self.carousel.append(section)
		firstCell = SECTION({'class':'carousel-cell text','style':'width:300px;'})
		firstCell.append(self.navigation)
		firstCell.append(self.socialIcons)
		self.carousel.prepend(firstCell)
		self.carousel.append(SECTION({'class':'carousel-cell'}))
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

		attrs = {'rel':'stylesheet','type':'text/css','media':'screen'}
		for href in ['webtype_fonts.min.css','flickity.min.css','mstocco.css']:
			attrs['href'] = '/assets/css/%s' % href
			self.head.append(LINK(attrs))
		
		self.head.append(SCRIPT({"src":"/assets/js/flickity.pkgd.min.js"}))
		self.head.append(SCRIPT({"src":"/assets/js/bg-lazyload.js"}))

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
		self.title = 'Mario Stocco'
		self.url = 'https://mariostoc.co/'

	def tohtml(self):
		anchor = A({"href":self.url})
		anchor.innerHTML = "&gt; %s" % self.url
		self.head.append(META({"http-equiv":"refresh","content":"1;url=%s" % self.url}))
		self.head.append(TITLE(self.title))
		self.body.append(anchor)
		self.documentElement.append(self.head)
		self.documentElement.append(self.body)
		return '%s%s' % (self.doctype, self.documentElement.tohtml())

