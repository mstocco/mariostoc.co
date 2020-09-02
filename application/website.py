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
		self.content = os.getcwd() + '/../content/'
		self.public = os.getcwd() + '/../docs'
		self.today = int(time.strftime('%Y%m%d', time.localtime()))

	def clean(self):
		print('\ncleaning...')
		for directory in ['blog','traininglog','racereports','pictures']:
			print('->', directory)
			targetdir = '%s/%s' % (self.public, directory)
			for filename in os.listdir(targetdir):
				target = '%s/%s' % (targetdir, filename)
				print('  - %s' % filename)
				os.remove(target)
		try:
			os.remove('%s/about' % self.public)
		except:
			pass

	def publish(self):
		print('\npublishing...')
		latestWritten = False
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
					if directory == '/traininglog':
						if not latestWritten:
							if self.today >= int(filename[:8]):
								redirect = RedirectDocument()
								redirect.title = 'Training Log Current Week'
								redirect.url = '/traininglog/%s' % filename.split('.md')[0]
								
								webpage = TemplateDocument()
								webpage.handleMarkdown('%s%s' % (self.content, basename))
								self.saveDocument(directory, 'index', webpage)
								latestWritten = True
				
		print('\ndone.')

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
		if target == 'index': targetpath = '%s.html' % targetpath
		print('  + ', target)
		html = webpage.tohtml()
		fileobj = open(targetpath, 'w', encoding='utf-8')
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

