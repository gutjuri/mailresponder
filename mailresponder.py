#coding: utf8
import imaplib
import email
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from datetime import datetime


acc = "YOUR-MAILACCOUNT@gmail.com"
pw = "YOUR-PASSWORD"

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(acc, pw)
mail.list()
mail.select("inbox")
result, data = mail.search(None, "ALL")
ids = data[0]
id_list = ids.split()

for mail_id in id_list:
	typ, data = mail.fetch(mail_id, '(RFC822)' )
	msg = email.message_from_string(data[0][1])
	varFrom = msg["from"]
	varSub = msg["subject"]
	# if you don't want all incoming messages deleted, comment out the following line
	mail.store(mail_id, '+FLAGS', '\\Deleted')
	with open("whitelist.txt") as f:
		addr = f.read().splitlines()
	send = True
	for ad in addr:
		if ad in varFrom and ad != "":
			send = False
	if send == True:
		res = MIMEMultipart()
		res['From'] = acc
		res['To'] = varFrom
		res['Subject'] = "AUTOMATED REPLY"
		res.attach(MIMEText("SAMPLE TEXT", 'plain'))
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(acc, pw)
		txt = res.as_string()
		server.sendmail(acc, varFrom, txt)
		server.quit()
		with open("mailresponder.log", "a") as log:
			log.write(varFrom + " at " + str(datetime.now()) + " (" + varSub + ")\n")
mail.expunge()
