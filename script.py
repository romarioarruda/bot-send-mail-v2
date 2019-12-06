#!/bin/bash/python3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import requests

response = requests.get('https://api.github.com/users/romarioarruda')
data = response.json()


from_addr = 'email@example1'
to_addr   = 'email@example2'

msg = MIMEMultipart()

msg['From'] = from_addr
msg['To'] = to_addr
msg['Subject'] = "Api data from github user [{}]".format(data['name'])

body = """ 
    <html>
        <body>
            <table style='width:500px' border='1'>
                <tr>
                    <th>User</th>
                    <th>Followers</th>
                    <th>Following</th>
                </tr>
                <tr style='text-align:center'>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                </tr>
            </table>
        </body>
    </html>
""".format(data['name'], data['followers'], data['following'])

#insert html
msg.attach(MIMEText(body, 'html'))

#Attachment
#Image just to representing example
filename = 'panfleto.pdf'

#file open
anexo = open(filename, 'rb')

#defined file type
base = MIMEBase('application', 'octet-stream')

#read from memory
base.set_payload((anexo).read())

#Enconding
encoders.encode_base64(base)

#Information default
base.add_header('Content-Disposition', 'attachment; filename = %s' % filename)

#Attachment at mail
msg.attach(base)

#smtp server and port
smtp = smtplib.SMTP('smtp.gmail.com', 587)

#safe
smtp.starttls()

#Login on account user
smtp.login(from_addr, 'your pass')

#string converting
text = msg.as_string()

#send mail
smtp.sendmail(from_addr, to_addr, text)

#close conection
smtp.quit()