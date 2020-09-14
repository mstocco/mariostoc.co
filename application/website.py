#!/usr/bin/python3
import os
import time
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
		self.content = os.getcwd() + '/../content'
		self.public = os.getcwd() + '/../docs'
		self.today = int(time.strftime('%Y%m%d', time.localtime()))
		self.setCurrentTrainingWeek()
	
	def setCurrentTrainingWeek(self):
		""" The current training week is referenced in a
		    document's <nav> element
		"""
		logfiles = os.listdir('%s/traininglog/' % self.content)
		logfiles.sort()
		for logfile in logfiles:
			if int(logfile[0:8]) > self.today:
				break
			self.current = '/traininglog/%s' % logfile[9:].split('.md')[0]
		return

	def clean(self):
		""" 1. Walk the specific directories in the public directory.
		    2. Delete files.
		    3. Hope that someone is about to re-publish very soon.
		"""
		print('\ncleaning...')
		for directory in ['blog','traininglog','racereports','pictures']:
			print('->', directory)
			targetdir = '%s/%s' % (self.public, directory)
			for root, dirs, files in os.walk(targetdir):

				for filename in files:
					target = '%s/%s' % (root, filename)
					print('  - %s' % target.replace(self.public, ''))
					os.remove(target)
		try:
			os.remove('%s/about' % self.public)
		except:
			pass

	def publish(self):
		""" 1. Walk the content directory looking for markdown files.
		    2. Convert markdown into an HTML5 Document
		    3. Try to save it under the public directory.
		"""
		print('\npublishing...')
		latestWritten = False
		for root, dirs, files in os.walk(self.content):
			directory = '%s' % root.split(self.content)[1]

			print('->', directory)
			files.sort()
			files.reverse()
			for filename in files:
				if filename.find('.md') > 1:
					if filename.find('.icloud') > 1:
						continue
					basename = '%s/%s' % (directory, filename)
					webpage = TemplateDocument()
					webpage.documentURI = basename.replace('.md', '')
					if len(filename) > 9:
						if filename[:8].isnumeric():
							webpage.lastModified = int(filename[:8])
							webpage.documentURI =webpage.documentURI.replace(filename[:9], '')
					elif filename == 'index.md':
						webpage.documentURI = basename.replace('.md', '.html')
					if hasattr(self, 'current'):
						if webpage.documentURI != self.current:
							webpage.navigation.current = {'href': self.current}
					webpage.handleMarkdown('%s%s' % (self.content, basename))
					self.saveDocument(webpage)
					continue

			if directory == '/traininglog':
				if hasattr(self, 'current'):
					redirect = RedirectDocument()
					redirect.url = self.current
					redirect.title = 'Latest Training Log Entry'
					redirect.documentURI = '/traininglog/latest'
					self.saveDocument(redirect)
		print('\ndone.')
		
	def saveDocument(self, webpage):
		""" Save the HTML5 Doc if it is new or its markdown
		    is different from a previous version.
		""" 
		target = '%s/%s' % (self.public, webpage.documentURI)
		if os.path.isfile(target):
			with open(target, 'r', encoding='utf-8') as htmlObj:
				parser = MetaTagParser()
				parser.parseHead(htmlObj.read())
				if hasattr(parser, 'version'):
					if parser.version == webpage.version:
						return
		else:
			filename = '%s' % target.split('/').pop()
			targetdir = target.split(filename)[0]
			try:
				os.makedirs(targetdir)
			except FileExistsError:
				pass
		print('  +', webpage.documentURI)
		html = webpage.tohtml()
		fileobj = open(target, 'w', encoding='utf-8')
		fileobj.write(html)
		fileobj.close()
		return
	
	def do(self):
		if hasattr(self, 'action'):
			if self.action == 'clean':
				return self.clean()
			if self.action == 'jpeg':
				return
		self.publish()
		return

if __name__ == '__main__':
	import argparse

	website = Website()
	## Command Line Argument Definitions
	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers(dest="action", help='________________________')
	subparsers.add_parser('clean', help='Removes previously published documents')
	subparsers.add_parser('publish', help='Walks the content directory and creates documents')
	subparsers.add_parser('jpeg', help='Resize, crop, file JPEG files')
	parser.parse_args(namespace=website)

	## Let's do this
	website.do()

