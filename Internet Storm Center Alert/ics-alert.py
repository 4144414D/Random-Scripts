#!/usr/bin/python2.7
#Adam Swann - github.com/4144414d

import smtplib
import urllib2
from email.mime.text import MIMEText

def email():
    s = smtplib.SMTP("smtp.gmail.com",587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login("username","password")
    msg = MIMEText('Something bad is happening on the internet - https://isc.sans.edu/')
    msg_from = 'from'
    msg_to = 'to'
    msg['Subject'] = 'Internet Storm Center Alert!'
    msg['From'] = msg_from
    msg['To'] = msg_to
    s.sendmail(msg_from, [msg_to], msg.as_string())
    s.quit()
    
if __name__ == '__main__':
    f = open('/scripts/last_status')
    last_status = f.read()
    f.close
    response = urllib2.urlopen('http://isc.sans.edu/infocon.txt')
    current_status = response.read()
    if current_status == "test": current_status = 'green'
    if (last_status != current_status) and (current_status != 'green'): email()
    f = open('/scripts/last_status','w')
    f.write(current_status)
    f.close