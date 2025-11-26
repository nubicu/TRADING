# -*- coding: utf-8 -*-
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import sys

fi = open("gmail_credentials.txt", "r")

# In order this connection to work, you need to activate the access for
# less secure applications at https://myaccount.google.com/lesssecureapps
try:
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo_or_helo_if_needed()
    server.starttls()
    server.ehlo_or_helo_if_needed()
    username = fi.readline().strip()
    password = fi.readline().strip()
#    print("Username:", username, " pass:", password)
    server.login(username, password)

    sender = fi.readline().strip()
    recipient = fi.readline().strip()
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = [sender, recipient]
    msg['Subject'] = "Email sent with Python app"
    body = "Salutare, B0$$!"
    msg.attach(MIMEText(body, 'plain'))

    text = msg.as_string()
    server.sendmail(msg['From'], msg['To'].split(","), text)
    server.quit()
    fi.close()

except smtplib.SMTPException:
    print("SMTPException\n")
    sys.exit()
except smtplib.SMTPConnectError:
    print("SMTPConnectError\n")
    sys.exit()
except smtplib.SMTPAuthenticationError:
    print("SMTPAuthenticationError\n")
    sys.exit()
except smtplib.SMTPNotSupportedError:
    print("SMTPNotSupportedError\n")
    sys.exit()