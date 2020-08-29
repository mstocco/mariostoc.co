#!/usr/bin/python3
import os
from templateDocument import *
from html.parser import HTMLParser



class MetaTagParser(HTMLParser):
	def parseHead(self, content):
		self.feed(content.split('</head>')[0])
		return

	def handle_starttag(self, tag, attrs):
		if tag == 'meta':
			if attrs[0][1] == 'x-version':
				self.version = attrs[1][1]


class Website:
	def __init__(self):
		self.content = os.getcwd() + '/../content/'
		self.public = os.getcwd() + '/../docs'

	def publish(self):
		for root, dirs, files in os.walk(self.content):
			directory = '/%s' % os.path.basename(root)
			print('->', directory)
			files.sort()
			files.reverse()
			for filename in files:
				basename = '%s/%s' % (os.path.basename(root), filename)
				if filename.find('.md') > 1:
					if filename.find('.icloud') > 1:
						continue
					webpage = TemplateDocument()
					webpage.handleMarkdown('%s%s' % (self.content, basename))
					self.saveDocument(directory, filename, webpage)
		print('done.')

	def saveDocument(self, directory, filename, webpage):
		target = filename.split('.md')[0]
		if len(target) > 9:
			if target[:8].isnumeric():
				target = '-'.join(target.split('-')[1:])
		directorypath = '%s%s' % (self.public, directory)
		targetpath = '%s/%s' % (directorypath, target)
		if os.path.isfile(targetpath):
			with open(targetpath, 'r', encoding='utf-8') as htmlObj:
				parser = MetaTagParser()
				parser.parseHead(htmlObj.read())
				if hasattr(parser, 'version'):
					if parser.version == webpage.version:
						return
		if not os.path.isdir(directorypath):
			try:
				os.makedirs(directorypath)
			except FileExistsError:
				pass
		print('  -> %s' % target)
		html = webpage.tohtml()
		fileobj = open(targetpath, 'w', encoding='utf-8')
		fileobj.write(html)
		fileobj.close()
		return

website = Website()
website.publish()
