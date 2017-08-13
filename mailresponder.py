#coding: utf8
import imaplib
import email
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


acc = "YOUR-ACCOUNT@gmail.com"
pw = "YOUR-PASSWORD"

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(acc, pw)
mail.list()
mail.select("inbox")
result, data = mail.search(None, "ALL")
ids = data[0]
id_list = ids.split()
latest_email_id = id_list[-1]
typ, data = mail.fetch(latest_email_id, '(RFC822)' )
for response_part in data:
	if isinstance(response_part, tuple):
		msg = email.message_from_string(response_part[1])
		varSubject = msg['subject']
		varFrom = msg['from']
mail.store(latest_email_id, '+FLAGS', '\\Deleted')
mail.expunge()


res = MIMEMultipart()
res['From'] = acc
res['To'] = varFrom
res['Subject'] = "Your E-Mail"

res.attach(MIMEText("YOUR-MESSAGE", 'plain'))
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(acc, pw)
txt = res.as_string()
server.sendmail(acc, varFrom, txt)
server.quit()
