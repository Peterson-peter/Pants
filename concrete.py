#!/bin/python

import requests
from lxml import html
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os

HD60 = "https://www.homedepot.com/p/SAKRETE-60-lb-Gray-Concrete-Mix-65200940/100321247"
HD80 = "https://www.homedepot.com/p/SAKRETE-80-lb-Gray-Concrete-Mix-65200390/100350291"

def send_email():
    #msg = email.message_from_string()
    msg = MIMEMultipart('alternative')
    msg['From'] = "ptp_is@Hotmail.com"
    msg['To'] = "ptp_is@Hotmail.com"
    msg['Subject'] = "Oven Found on Sale"
    s = smtplib.SMTP("smtp.live.com",587)
    html = "<html><head></head><body><h3>Go look at ovens</h3><p><p> \
    <table><tr><th>Weight</th><th>price</th><th>URL</th></tr> \
    <tr><td>60Lbs</td><td>"+get_hd(HD60)+"</td><td>"+HD60+"</td></tr> \
    <tr><td>80Lbs</td><td>"+get_hd(HD80)+"</td><td>"+HD80+"</td></tr> \
    </table></body></html>"
    parts = MIMEText(html, 'html')
    msg.attach(parts)
    s.ehlo() # Hostname to send for this command defaults to the fully qualified domain name of the local host.
    s.starttls() #Puts connection to SMTP server in TLS mode
    s.login('ptp_is@hotmail.com', os.environ["email"])
    s.sendmail("ptp_is@hotmail.com","ptp_is@hotmail.com", msg.as_string())
    s.quit()


def get_hd(url):
    response = requests.get(url)
    tree = html.fromstring(response.content)
    price = tree.xpath('//span[@class="pReg"]/text()')
    return price[0].split("$")[1][:4]

def main():
        sixty = get_hd(HD60)
        print("Price check on 60lbs is: $"+ sixty)
        eighty = get_hd(HD80)
        print("Price check on 80lbs is: $"+ eighty)
        if float(sixty) < 3.1:
            send_email()
        if float(eighty) < 3.9:
            send_email()



if __name__ == '__main__':
    main()
