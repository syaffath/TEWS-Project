import imaplib
import base64
import os
import email
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
import sys
from PIL import Image
from email.header import decode_header
import ctypes

email_user = 'rilo.songorayyan@gmail.com'
email_pass = 'rilopambudialiyyin'
 


def import_messages(Body_email, Time):
    status, messages = mail.select("INBOX")
    N = 1
    messages = int(messages[0])
    global subject

    
    for i in range(messages, messages-N, -1):
        res, msg = mail.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding)
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            Body_email.append(body)
                            Time.append(msg['Date'])
                        elif "attachment" in content_disposition:
                            filename = part.get_filename()
                            if filename:
                                folder_name = clean(subject)
                                if not os.path.isdir(folder_name):
                                    os.mkdir(folder_name)
                                filepath = os.path.join(folder_name, filename)
                                open(filepath, "wb").write(part.get_payload(decode=True))
                else:
                    content_type = msg.get_content_type()
                    body = msg.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        Body_email.append(body)
                        Time.append(msg['Date'])

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)
N0 = 0
import time
while (True):
    mail = imaplib.IMAP4_SSL("imap.gmail.com",993)
    mail.login(email_user, email_pass)
    mail.select('"Inbox"')
    _,data = mail.search(None, 'ALL')    

    Body_email = []
    Time = []
    
    import_messages(Body_email, Time)
    
    ID_email = int(subject)
    
    N1 = ID_email
    
    if N0 != N1:
        email_rilo = [Body_email[0], Time[0]]
        email_rilo_str = '\n'.join(map(str, email_rilo))
        if email_rilo_str.__contains__('Tsunami'):
            Mbox('Alert!!', email_rilo_str, 1)
        else: 
            pass
    else:
        pass
    N0 = N1
    time.sleep(0)
