#!/usr/bin/python3

## Classes that make up the two basic elements of a webpage:
##   The Document and the Elements it contains.
##
## Both classes have a tohtml() method that returns the 
## string representation of the class, formatted as 
## valid HTML5.


class HTML5Document:
	""" A very minimalistic impmlementation of an HTML DOM Document.
	    There is a DOCTYPE declaration and an HTML element that
	    contains a HEAD and BODY element.  The title attribute gets
	    written in as a TITLE element when the tohtml() methods is
	    called.
	     
	"""
	def __init__(self):
		self.doctype = '<!DOCTYPE html>'
		self.documentElement = HTML({'lang':'en'})
		self.head = HEAD()
		self.body = BODY()
		self.title = ''
		self.characterSet = 'utf-8'
		if callable(self.template):
			self.template()

	def tohtml(self):
		""" Put it all together and print to stdout.
		"""
		self.head.prepend(TITLE(self.title))
		self.documentElement.append(self.head)
		self.documentElement.append(self.body)
		return '%s%s' % (self.doctype, self.documentElement.tohtml())


class HTML5Tag:
	""" A very lightweight representation of a DOM Element.
	    Unlike a DOM Element, this object intensionally has no
	    idea about its "children"; instead it uses an "innerHTML"
	    string variable that can be appended or prepended to.
	"""
	def __init__(self, arg=''):
		self.innerHTML = ''
		self.length = 0
		if (type(arg) == dict):
			for key, value in arg.items():
				if key in ('id', 'class', 'type'):
					setattr(self, '_%s' % key, value)
					continue
				setattr(self, key, value)
		else:
			self.append(arg)
	
	def attributes(self):
		""" Unlike a DOM Element, attributes is a method that
		    returns a string instead of a list property.
		"""
		attrs = []
		for key, value in self.__dict__.items():
			if key in ('tagname', 'innerHTML', 'length'):
				continue
			if isinstance(value, str):
				if key[0] == '_': key = key[1:]
				key = key.replace('_', '-')
				attrs.append('%s="%s"' % (key, value))
		if len(attrs) > 0:
			return ' %s' % ' '.join(attrs)
		return ''

	def append(self, arg):
		tohtml = getattr(arg, "tohtml", None)
		if callable(tohtml):
			self.innerHTML = self.innerHTML + arg.tohtml()
		else:
			self.innerHTML = self.innerHTML + (arg)
		self.length = len(self.innerHTML)
		return

	def prepend(self, arg):
		tohtml = getattr(arg, "tohtml", None)
		if callable(tohtml):
			self.innerHTML = arg.tohtml() + self.innerHTML
		else:
			self.innerHTML = str(arg) + self.innerHTML
		self.length = len(self.innerHTML)
		return

	def tohtml(self):
		tagname = self.__class__.__bases__[0].__name__.lower()
		if tagname == 'html5tag':
			tagname = self.__class__.__name__.lower()
		unpaired = ['base','meta','link','hr','br','input','img']
		if tagname in unpaired:
			return '<%s%s />' % (tagname, self.attributes())
		return '<%s%s>%s</%s>' % (tagname, self.attributes(), self.innerHTML, tagname)


## _____________________________________
## Some Named HTML5 Tags below

class A(HTML5Tag): pass
class ABBR(HTML5Tag): pass
class ADDRESS(HTML5Tag): pass
class ARTICLE(HTML5Tag): pass
class ASIDE(HTML5Tag):pass
class B(HTML5Tag): pass
class BASE(HTML5Tag): pass
class BLOCKQUOTE(HTML5Tag): pass
class BODY(HTML5Tag): pass
class BR(HTML5Tag): pass
class AUDIO(HTML5Tag): pass
class ASIDE(HTML5Tag): pass
class ARTICLE(HTML5Tag): pass
class BLOCKQUOTE(HTML5Tag): pass
class DIV(HTML5Tag): pass
class EM(HTML5Tag): pass
class FOOTER(HTML5Tag): pass
class FORM(HTML5Tag): pass
class H1(HTML5Tag): pass
class H1(HTML5Tag): pass
class H2(HTML5Tag): pass
class H3(HTML5Tag): pass
class H4(HTML5Tag): pass
class H5(HTML5Tag): pass
class H6(HTML5Tag): pass
class HEAD(HTML5Tag): pass
class HEADER(HTML5Tag): pass
class HR(HTML5Tag): pass
class HTML(HTML5Tag): pass
class I(HTML5Tag): pass
class IMG(HTML5Tag): pass
class INPUT(HTML5Tag): pass
class LI(HTML5Tag): pass
class LINK(HTML5Tag): pass
class MAIN(HTML5Tag): pass
class META(HTML5Tag): pass
class NAV(HTML5Tag): pass
class H1(HTML5Tag): pass
class P(HTML5Tag): pass
class PATH(HTML5Tag): pass
class S(HTML5Tag): pass
class SCRIPT(HTML5Tag): pass
class SECTION(HTML5Tag): pass
class SMALL(HTML5Tag): pass
class STRONG(HTML5Tag): pass
class STYLE(HTML5Tag): pass
class SUB(HTML5Tag): pass
class SUP(HTML5Tag): pass
class SVG(HTML5Tag): pass
class TITLE(HTML5Tag): pass
class UL(HTML5Tag): pass
class WBR(HTML5Tag): pass
