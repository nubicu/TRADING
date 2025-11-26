# -*- coding: utf-8 -*-
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import sys

fi = open("other_credentials.txt", "r")

try:
    print("Please wait!")
    server = smtplib.SMTP(host="mail.vfemail.net:587")
    server.ehlo_or_helo_if_needed()
    server.starttls()
    server.ehlo_or_helo_if_needed()
    username = fi.readline()
    password = fi.readline().strip()
#    print("Username:", username, " pass:", password)
    server.login(username, password)
    print("Connected to server!")

    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = fi.readline()
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

    print("Done")