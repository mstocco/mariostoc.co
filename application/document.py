#!/usr/bin/python3
from innerHTML import *


class Document:
	""" A very minimalistic impmlementation of an HTML DOM Document.
	    There is a DOCTYPE declaration and an HTML element that
	    contains a HEAD and BODY element.  The title attribute gets
	    written in as a TITLE element when the tohtml() methods is
	    called.
	     
	"""
	def __init__(self, directory, filename):
		self.doctype = '<!DOCTYPE html>'
		self.documentElement = HTML({'lang':'en'})
		self.title = ''
		self.documentURI = '%s/%s' % (directory, filename.split('.md')[0])
		if len(filename) > 9:
			if filename[:8].isnumeric():
				self.documentURI = self.documentURI.replace(filename[:9], '')
		elif filename == 'index.md':
			self.documentURI = '%s/index.html' % (directory)
			self.nocache = True
		self.head = HEAD()
		self.body = BODY()
		self.characterSet = 'utf-8'
	
	def tohtml(self):
		self.head.prepend(TITLE(self.title))
		self.documentElement.append(self.head)
		self.documentElement.append(self.body)
		return '%s%s' % (self.doctype, self.documentElement.tohtml())

	def write(self, content):
		self.body.innerHTML = content
		return
	
	def save(self, public):
		fileobj = open('%s%s' % (public, self.documentURI), 'w')
		fileobj.write(self.tohtml())
		fileobj.close()
		return


class RedirectDocument(Document):
	def tohtml(self):
		anchor = A({"href":self.url})
		anchor.innerHTML = " %s" % self.url
		forward = P('This page is trying to send you to ')
		forward.append(anchor)

		anchor = A({'href':'#','onclick':'history.back();'})
		anchor.innerHTML = 'return to the previous page.'
		backward = P('If you do not want to visit that page, you can ')
		backward.append(anchor)
		self.head.append(META({"http-equiv":"Pragma","content":"no-cache"}))
		self.head.append(META({"http-equiv":"Expires","content":"-1"}))
		self.head.append(META({"http-equiv":"Refresh","content":".3;url=%s" % self.url}))
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

