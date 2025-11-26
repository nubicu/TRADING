# -*- coding: utf-8 -*-
import imaplib
import email
import html2text
import os

dir = os.getcwd()
os.chdir(dir)

fi = open(r"/media/nubicu/Data/NU_STERGE/Robert/Work/Python/Learning/WebRelated/gmailcredentials.txt")
fo = open("gmail_emails.txt", "w", encoding="utf-8")

# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------
FROM_EMAIL = fi.readline().strip() + "@gmail.com"
FROM_PWD = fi.readline().strip()
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993

h = html2text.HTML2Text()
h.ignore_links = True
h.ignore_anchors = True
h.ignore_images = True

try:
    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(FROM_EMAIL, FROM_PWD)
    mail.select('inbox')

    type, data = mail.search(None, 'ALL')
    mail_ids = data[0]

    id_list = mail_ids.split()
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])

    for i in range(latest_email_id, first_email_id, -1):
        typ, data = mail.fetch(str(i), '(RFC822)')

        for response_part in data:
            if isinstance(response_part, tuple):
                dt = "utf-8"
                msg = email.message_from_string(response_part[1].decode(dt))
                email_subject = msg['subject']
                email_from = msg['from']
                fo.write("From:" + email_from + " Subject:" + email_subject)
                for part in msg.walk():
# each part is a either non-multipart, or another multipart message
# that contains further parts... Message is organized like a tree
                    if part.get_content_type() == 'text/plain':
# prints the raw text
                        fo.write(part.get_payload().strip(' \t\n\r'))
                    #elif part.get_content_type() == 'text/html':
                        #fo.write(h.handle(part.get_payload()))

except Exception as e:
    print(str(e))

fi.close()
fo.close()