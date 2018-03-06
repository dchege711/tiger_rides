import smtplib
import os
# Import the email modules we'll need
from email.message import Message
email_address = 'komrons@princeton.edu'

def sample_send(me, you,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    msg = Message()
    # me == the sender's email address
    # you == the recipient's email address
    msg.set_payload('Now go to the login page.')
    msg['Subject'] = 'Welcome to Tiger_rides!'
    msg['From'] = me
    msg['To'] = you
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(me, you, msg.as_string())
    server.quit()

sample_send(me    = 'tiger.rides123@gmail.com',
              you = 'komrons@princeton.edu',
              login        = 'tiger.rides123',
              password     = os.environ["TIGER_RIDES_EMAIL_PASSWORD"])
