from utils import util
from core import *
import datetime
import smtplib

def authenticate():
    f = open(util.get_mangagrabber_dir() + 'auth.txt', 'r')
    lines = f.readlines()
    lines[0] = lines[0].replace('\n', '')
    lines[1] = lines[1].replace('\n', '')

    email = lines[0]
    pw = lines[1]

    return email, pw

def ez_send_email(receivers, content, update_info=None):
    email, pw = authenticate()
    send_email(email, pw, receivers, content, update_info)

def send_email(email, pw, receivers, content, update_info=None):
    gmail_user = email
    gmail_pwd = pw
    FROM = email
    TO = receivers
    TIME = datetime.date.today()
    SUBJECT = "New manga has been released! --- " + str(TIME)

    if update_info is not None:
        content = html(update_info)

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, content)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.quit()
        print 'successfully sent the mail'
    except Exception as e:
        print e
        print "failed to send mail"
