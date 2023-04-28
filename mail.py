from bs4 import BeautifulSoup
import requests
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

URL = "https://ficlit.unibo.it/it/eventi"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

events = soup.find_all("a", class_="item None active")
descs = ''
for event in events:
    link = event.get('href')
    dateel = event.find('div', class_="date") \
                if event.find('div', class_="date")\
                else event.find('div', class_="period") if event.find('div', class_="period") \
                else '<p>senza data</p>'

    desc = event.find('div', class_="text-wrap") if event.find('div', class_="text-wrap") else ''
    descs += dateel.prettify() + desc.prettify() + "<a target='_blank' href='"+link+"'>Leggi di più</a><hr/>"

sender_address = "comunicazioneficlit@live.unibo.it"
receiver_address = "ficlit.all@unibo.it"
port = 25
smtp_server = "" # add server

message = MIMEMultipart("")
message["Subject"] = "FICLIT:News. La newsletter settimanale degli eventi del FICLIT"
message["From"] = sender_address
message["To"] = receiver_address

# Create the HTML version of your message
html = """\
<html>
  <body>
    <p>Gentilissime e gentilissimi, <br/>ecco gli eventi delle prossime settimane organizzati dal FICLIT:</p>
    """+descs+"""
    <hr/>
    <p>Questa mail è generata automaticamente, si prega di non rispondere</p>
    <hr/>
  </body>
</html>
"""

# Create both plain and HTML text objects
part2 = MIMEText(html, "html")

# Attach both versions to the outgoing message
message.attach(part2)

# Send the email with your SMTP server
context = ssl.create_default_context()

with smtplib.SMTP(smtp_server,port) as server:
   server.sendmail(sender_address,receiver_address.split(','),message.as_string())
