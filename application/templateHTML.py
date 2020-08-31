#!/usr/bin/python3
from innerHTML import *
from markdown2 import markdown

## _____________________________________
## Templated HTML5 Tag Definitions

class Masthead(HEADER):
	""" Seen above the Carousel.
	    This toogles the site navigation and provides a
	    link to the home page.
	"""
	def __init__(self):
		self._class = 'masthead'
		a1 = A({"href":"javascript:toggle();"})
		a1.append(IMG({"src":"/assets/img/guideicon.svg","class":"guide-icon"}))
		self.innerHTML = a1.tohtml()
		
		a2 = A({"href":"/","class":"mariostocco"})
		a2.append("MARIO STOCCO")
		self.append(a2)


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


class CarouselText(SECTION):
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


class CarouselImage(SECTION):
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
		try:
			self.width = int(url.split('/')[-1].split('x')[0])
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
		self.links.append({'href':'/about', 'label':'ABOUT'})
		input1 = INPUT({"name":"q","id":"q","type":"text","maxlength":"200","placeholder":"search..."})
		input2 = INPUT({"name":"q","type":"hidden","value":"site:mariostoc.co"})
		google = FORM({"action":"https://google.com/search"})
		google.append(input1)
		google.append(input2)
		self.innerHTML = google.tohtml()

	def tohtml(self):
		ul = UL({"class":"alt"})
		for attrs in self.links:
			anchor = A({'href':attrs['href']})
			anchor.innerHTML = attrs['label']

			li = LI({"class":"item"})
			li.append(anchor)
			ul.append(li)
		self.append(ul)
		return HTML5Tag.tohtml(self)


class SocialIcon(LI):
	""" This is this list item element that contains an
		anchor tag that points to an account that I have
		somewhere else on the inter-webs.
	"""
	def __init__(self, alt, href):
		self._class = 'icon'		
		src = '/assets/img/%s.svg' % alt.lower()
		anchor = A({"href":href,"target":"_blank"})
		anchor.append(IMG({"src":src,"alt":alt}))
		self.innerHTML = anchor.tohtml()


class SocialIcons(DIV):
	""" There are 5 links to account pages on other sites.
	    They are displayed in this DIV tag which is found
	    at the bottom of the carousel's first cell.
	"""
	def tohtml(self):
		ul = UL()
		ul.append(SocialIcon('Strava', 'https://www.strava.com/athletes/21702937'))
		ul.append(SocialIcon('Garmin', 'https://connect.garmin.com/modern/profile/_canadian'))
		ul.append(SocialIcon('Twitter', 'https://twitter.com/vaporfly4pct'))
		ul.append(SocialIcon('Linkedin', 'https://www.linkedin.com/in/voipexpert'))
		ul.append(SocialIcon('GitHub', 'https://github.com/mstocco'))
		self.append(P('SOCIALLY PROFILED'))
		self.append(ul)
		self._class = 'social'
		return HTML5Tag.tohtml(self)


class PageFooter(FOOTER):
	""" Footer for the bottom of the webpage.
	"""
	def tohtml(self):
		copyright = P("Copyright &copy; 2020 Mario Stocco &nbsp; All rights reserved.")
		self.append(copyright)
		return HTML5Tag.tohtml(self)

class FlickityJS(SCRIPT):
	""" Javascript Tag included in the body of the document.
	"""
	def tohtml(self):
		self._type = 'text/javascript'
		self.append("var elem=document.getElementById('carousel');")
		self.append("var flkty=new Flickity(elem,{")
		self.append(" prevNextButtons:false,")
		self.append(" cellAlign:'left',")
		self.append(" bgLazyLoad:3,")
		self.append(" pageDots:false,")
		self.append(" accessibility:true,")
		self.append(" contain:1,")
		self.append(" initialIndex:1,")
		self.append(" imagesLoaded:true,")
		self.append(" freeScroll:true")
		self.append("});")
		self.append("function toggle(){if(flkty.selectedIndex>0){flkty.select(0);}else{flkty.select(1);}};")
		return HTML5Tag.tohtml(self)

