#!/usr/bin/env python
from lxml import html
import requests
from time import sleep
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def get_current_price():
    url = "http://www.levi.com/US/en_US/category/sale/men/itemtype/jeans/waist/36/length/29/"
    page = requests.get(url)
    tree = html.fromstring(page.content)
    name = tree.xpath('//p[@class="name"]/text()')
    color = tree.xpath('//p[@class="finish"]/text()')
    salePrices = tree.xpath('//span[@class="pSale"]/text()')
    OrgPrices = tree.xpath('//span[@class="pWas2"]/text()')
    return {"name":name, "color":color, "salePrices":salePrices, "OrgPrices":OrgPrices}

def write_emailfile(name, color, salePrices,OrgPrices):
    z = 0
    with open("emailtext.html","a") as emailfile:
        emailfile.write("<html><head></head><body><table>")
        emailfile.write("<tr><th>Name</th><th>Color</th><th>Sale Price</th><th>Org Price</th></tr>")
        while z != len(name):
            if float(salePrices[z].encode('utf-8').split("$")[1]) < 15:
                emailfile.write("<tr bgcolor='#FF0000'>")
            elif float(salePrices[z].encode('utf-8').split("$")[1]) < 20:
                emailfile.write("<tr bgcolor='#FFFF00'>")
            elif float(salePrices[z].encode('utf-8').split("$")[1]) / float(OrgPrices[z].encode('utf-8').split("$")[1]) > .75:
                emailfile.write("<tr bgcolor='#00FF00'>")
            else:
                emailfile.write("<tr>")
            emailfile.write("<td>")
            emailfile.write(name[z].encode('utf-8'))
            emailfile.write("</td>")
            emailfile.write("<td>")
            emailfile.write(color[z].encode('utf-8'))
            emailfile.write("</td>")
            emailfile.write("<td>")
            emailfile.write(salePrices[z].encode('utf-8'))
            emailfile.write("</td>")
            emailfile.write("<td>")
            emailfile.write(OrgPrices[z].encode('utf-8'))
            emailfile.write("</td></tr>")
            z = z + 1
        emailfile.write("</table></body></html>")

def send_email():
    #msg = email.message_from_string()
    msg = MIMEMultipart('alternative')
    msg['From'] = "Jeans_checker@hotmail.com"
    msg['To'] = "ptp_is@Hotmail.com"
    msg['Subject'] = "New Jeans on sale"
    s = smtplib.SMTP("smtp.live.com",587)
    html = open('emailtext.html').read()
    parts = MIMEText(html, 'html')
    msg.attach(parts)
    s.ehlo() # Hostname to send for this command defaults to the fully qualified domain name of the local host.
    s.starttls() #Puts connection to SMTP server in TLS mode
    s.login('ptp_is@hotmail.com', os.environ["email"])
    s.sendmail("ptp_is@hotmail.com","ptp_is@hotmail.com", msg.as_string())
    s.quit()

def main():
    while True:
	print "starting"
        current = get_current_price()
	print "found "+ len(current['name']) + " items"
        sleep(21600)
        new = get_current_price()
        if current != new:
            print "found new items"
            write_emailfile(new['name'],new['color'],new['salePrices'],new['OrgPrices'])
            send_email()
            current = new


if __name__ == '__main__':
    main()
