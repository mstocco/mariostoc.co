import os
import json
from datetime import datetime
from document import Document, RedirectDocument
from innerHTML import *
from flickity import *

class StaticSiteGenerator:
	def __init__(self, domain):
		self.domain = domain
		self.content = os.getcwd() + '/../content'
		self.public = os.getcwd() + '/../docs'
		self.now = datetime.today()

	def do(self):
		if hasattr(self, 'action'):
			if self.action == 'clean':
				return self.clean()
			if self.action == 'redeploy':
				self.clean()
		self.deploy()
		return

	def clean(self):
		""" 1. Walk the content directory looking for markdown files.
		    2. Delete files generated from a markdown file.
		"""
		for root, dirs, files in os.walk(self.content):
			directory = '%s' % root.split(self.content)[1]
			filenames = []
			for filename in files:
				if filename.find('.icloud') > 0: continue
				if filename.split('.')[-1] == 'md': filenames.append(filename)
			filenames.sort()
			print('->', directory)
			for filename in filenames:
				document = Document(directory, filename)
				published = '%s%s' % (self.public, document.documentURI)
				if os.path.isfile(published):
					print(' ---', document.documentURI, '(delete todo)')
					os.remove(published)
		return

	def deploy(self):
		""" 1. Walk the content directory looking for markdown files.
		    2. Convert markdown into an HTML5 Documents.
		    3. Save that HTML file in the public directory.
		    4. Create new sitemap.txt and humans.txt files.
		"""
		modified = False
		traininglog = False
		for root, dirs, files in os.walk(self.content):
			directory = '%s' % root.split(self.content)[1]
			filenames = []
			for filename in files:
				if filename.find('.icloud') > 0: continue
				if filename.split('.')[-1] == 'md': filenames.append(filename)
			filenames.sort()
			if directory == '/traininglog' : trainingfiles = filenames

			if len(directory) > 0:
				print('->', directory)
				if not os.path.isdir('%s%s' % (self.public, directory)):
					print(' >>>', directory, ' (new directory)')
					os.mkdir('%s%s' % (self.public, directory))
			else:
				print('-> /')
			for filename in filenames:
				document = FlickityDocument(directory, filename)
				published = '%s%s' % (self.public, document.documentURI)
				if os.path.isfile(published):
					pubtime = os.path.getmtime(published)
					modtime = os.path.getmtime('%s/%s' % (root, filename))
					if (modtime > pubtime):
						## Rewrite webpage with newer content
						modified = True
						if directory == '/traininglog' :
							traininglog = True
							document.head.append('<script src="/assets/js/trainingcalendar.js"></script>');
							document.body.onload = "javascript:fetchActiveDays(trainingweek);"
						document.domain = self.domain
						document.lastModified = datetime.fromtimestamp(modtime).ctime()
						document.handleMarkdown('%s/%s' % (root, filename))
						document.save(self.public)
						print(' >>>', document.documentURI, ' mod:', document.lastModified)
				else:
					## Create new static webpage
					modified = True
					if directory == '/traininglog' : traininglog = True
					document.domain = self.domain
					document.lastModified = datetime.now().ctime()
					document.handleMarkdown('%s/%s' % (root, filename))
					document.save(self.public)
					print(' +++', document.documentURI, '(new)')
		
		if modified:
			if traininglog:
				self.saveActiveDays(trainingfiles)
				self.saveRedirects(trainingfiles)
			self.saveSiteMap()
			self.saveHumansTxt()
		return

	def redeploy(self):
		self.clean()
		self.deploy()
		return

	def saveSiteMap(self):
		sitemap = []
		for root, dirs, files in os.walk(self.public, topdown=True):
			for hidden in ['assets','pictures']:
				if hidden in dirs: dirs.remove(hidden)
			dirs = dirs.sort()

			urls = []
			directory = '%s' % root.split(self.public)[1]
			if 'index.html' in files:
				files.remove('index.html')
				urls.append('https://%s%s/' % (self.domain, directory))
				
			for filename in files:
				if filename[0] == '.': continue
				if filename.find('.htm') > 0: continue
				if filename.find('.ico') > 0: continue
				if filename.find('.jso') > 0: continue
				urls.append('https://%s%s/%s' % (self.domain, directory, filename))
			
			urls.sort()
			for url in urls:
				sitemap.append(url)

		print(' >>> /sitemap.txt')
		fileobj = open('%s/sitemap.txt' % self.public, 'w', encoding='utf-8')
		fileobj.write('\n'.join(sitemap))
		fileobj.close()
		return

	def saveHumansTxt(self):
		humans = []
		humans.append('/* AUTHOR */')
		humans.append('  Name: Mario Stocco')
		humans.append('  Site: https://mariostoc.co/')
		humans.append('  Location: Victoria, BC, Canada')
		humans.append('')
		humans.append('/* SITE */')
		humans.append('  Last update: %s' % self.now.strftime('%Y/%m/%d'))
		humans.append('  Language: English')
		humans.append('  Doctype: HTML5')
		humans.append('  Content Management: git')
		humans.append('  Created With: An Apple 11" iPad Pro and bit of Python')
		humans.append('')
		humans.append('/* THANKS */')
		humans.append('  Name: David DeSandro, https://github.com/metafizzy/flickity')
		humans.append('')
		
		print(' >>> /humans.txt')
		fileobj = open('%s/humans.txt' % self.public, 'w', encoding='utf-8')
		fileobj.write('\n'.join(humans))
		fileobj.close()
		return

	def saveActiveDays(self, filenames):
		active = {'totaldays':0, 'activedays':[], 'offdays':[]}
		for filename in filenames:
			yyyy = int(filename[:4])
			if yyyy < 2024 and filename.find('triathlon') == -1: continue

			weekday = False
			with open('%s/traininglog/%s' % (self.content, filename), 'r', encoding="utf-8") as logfile:
				lines = logfile.readlines()
			for line in lines:
				line = line.strip()
				for day in ['SUN','MON','TUE','WED','THU','FRI','SAT']:
					if line.find('## %s' % day) == 0:
						weekday = True
						datestr = '%s-%s' % (yyyy, '-'.join(line.split(' ')[2:4]))
				if weekday and line.find('Time: **') > -1:
					if line.find('Time: **0') == -1:
						dateobj = datetime.strptime(datestr, "%Y-%b-%d")
						active['activedays'].append(int(dateobj.strftime("%Y%m%d")))
		if len(active['activedays']) > 0:
			start = datetime.strptime(str(active['activedays'][0]), '%Y%m%d')
			last = datetime.strptime(str(active['activedays'][-1]), '%Y%m%d')
			active['totaldays'] = (last - start).days

		print(' >>> /assets/activedays.json  activedays: %d' % len(active['activedays']))
		fileobj = open('%s/assets/activedays.json' % self.public, 'w', encoding="utf-8")
		fileobj.write(json.dumps(active))
		fileobj.close()
		return

	def saveRedirects(self, filenames):
		today = int(self.now.strftime('%Y%m%d'))
		for index in range(len(filenames)):
			if int(filenames[index][:8]) > today: break
	
		for name, delta in (('latest',0), ('prevoius',1)):
			document = RedirectDocument('/traininglog', name)
			document.title = '%s Training Week' % name.capitalize()
			document.url = filenames[(index - delta)][9:].split('.md')[0]
			if delta == 0:
				if ((index + 1) <  len(filenames)):
					document.url += '?%s' % self.now.strftime('%a').lower()
			document.save(self.public)
			print(' >>> %s  %s' % (document.documentURI, document.url))
		return
