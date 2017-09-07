#!/usr/bin/python

#coding: utf8
import imaplib
import email
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from datetime import datetime


acc = 'YOUR-MAIL-ACCOUNT'
pw = 'YOUR-PW'

# insert the correct paths for these files below
logfile = 'mailresponder.log'
adresses = 'whitelist.txt'

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(acc, pw)
mail.list()
mail.select('inbox')
result, data = mail.search(None, 'ALL')
ids = data[0]
id_list = ids.split()

for mail_id in id_list:
	typ, data = mail.fetch(mail_id, '(RFC822)' )
	msg = email.message_from_string(data[0][1])
	varFrom = msg['from']
	varSub = msg['subject']
	mail.store(mail_id, '+FLAGS', '\\Deleted')
	with open(logfile, 'a') as log:
		log.write('\ndel: ' + varFrom + ' at ' + str(datetime.now()) + ' (' + varSub + ')\n')
	with open(adresses) as f:
		addr = f.read().splitlines()
	send = True
	for ad in addr:
		if ad in varFrom and ad != '':
			send = False
	if send == True:
		res = MIMEMultipart()
		res['From'] = acc
		res['To'] = varFrom
		res['Subject'] = 'YOUR-SUBJECT'
		res.attach(MIMEText('YOUR-MESSAGE', 'plain'))
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(acc, pw)
		txt = res.as_string()
		server.sendmail(acc, varFrom, txt)
		server.quit()
		with open(logfile, 'a') as log:
			log.write('res: ' + varFrom + ' at ' + str(datetime.now()) + ' (' + varSub + ')\n')
mail.expunge()
