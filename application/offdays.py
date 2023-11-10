
import os
import json
from datetime import datetime, timezone

class Offdays:
	def __init__(self):
		os.chdir('/home/mstocco/mariostoc.co/application')
		self.public = os.getcwd() + '/../docs'
		self.asset = '%s/assets/offdays.json' % self.public

		if not os.path.isfile(self.asset):
			fileobj = open(self.asset, 'w')
			fileobj.write('{"offdays":[]}')
			fileobj.close()

		self.offdays = json.load(os.popen('cat %s' % self.asset, 'r'))
		print(self.offdays)

	def commit(self):
		fileobj = open(self.asset, 'w')
		fileobj.write(json.dumps(self.offdays))
		fileobj.close()

	def add(self, date):
		self.offdays['offdays'].append(date)
		print(json.dumps(self.offdays))
		
offdays = Offdays()
raise SystemExit


offdays.add(20231018)
offdays.add(20231019)
offdays.add(20231020)
offdays.add(20231021)
offdays.add(20231022)
offdays.add(20231023)
offdays.add(20231024)
offdays.add(20231025)
offdays.add(20231026)
offdays.add(20231027)
offdays.add(20231028)
offdays.add(20231029)
offdays.add(20231030)
offdays.add(20231031)
offdays.add(20231101)
offdays.add(20231102)
offdays.add(20231103)
offdays.add(20231104)
offdays.add(20231105)
offdays.add(20231106)
offdays.add(20231107)
offdays.add(20231108)
offdays.add(20231109)
offdays.add(20231110)
offdays.add(20231111)
offdays.commit()
