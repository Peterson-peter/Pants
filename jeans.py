#!/usr/bin/env python
from lxml import html
import requests
from time import sleep
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os

def get_current_price():
    url = "https://www.levi.com/US/en_US/sale/mens-sale/jeans/c/levi_clothing_men_sale_jeans_us/facets/waist/36/length/29"
    page = requests.get(url)
    tree = html.fromstring(page.content)
    name = tree.xpath('//a[@class="name"]/text()')
    i = 0
    while i < len(name):
        name[i] = name[i].replace("\r\n\t\t\t\t\t","")
        name[i] = name[i].replace("\u2122","")
        name[i] = name[i].encode('utf-8')
        i = i+1
    color = tree.xpath('//div[@class="color-name"]/text()')
    salePrices = tree.xpath('//span[@class="hard-sale"]/text()')
    OrgPrices = tree.xpath('//span[@class="regular"]/text()')
    return {"name":name, "color":color, "salePrices":salePrices, "OrgPrices":OrgPrices}

def write_emailfile(name, color, salePrices,OrgPrices,filename):
    z = 0
    with open(filename,"a") as emailfile:
        emailfile.write("<html><head></head><body><table>")
        emailfile.write("<tr><th>Name</th><th>Color</th><th>Sale Price</th><th>Org Price</th></tr>")
        while z != len(name):
            if float(salePrices[z].split("$")[1]) / float(OrgPrices[z].split("$")[1]) < .50:
                emailfile.write("<tr bgcolor='#FF0000'>")
            elif float(salePrices[z].split("$")[1]) / float(OrgPrices[z].split("$")[1]) < .70:
                emailfile.write("<tr bgcolor='#FFFF00'>")
            elif float(salePrices[z].split("$")[1]) / float(OrgPrices[z].split("$")[1]) < .75:
                emailfile.write("<tr bgcolor='#00FF00'>")
            else:
                emailfile.write("<tr>")
            emailfile.write("<td>")
            emailfile.write(name[z])
            emailfile.write("</td>")
            emailfile.write("<td>")
            emailfile.write(color[z])
            emailfile.write("</td>")
            emailfile.write("<td>")
            emailfile.write(salePrices[z])
            emailfile.write("</td>")
            emailfile.write("<td>")
            emailfile.write(OrgPrices[z])
            emailfile.write("</td></tr>")
            z = z + 1
        emailfile.write("</table></body></html>")

def send_email():
    #msg = email.message_from_string()
    msg = MIMEMultipart('alternative')
    msg['From'] = "ptp_is@Hotmail.com"
    msg['To'] = "ptp_is@Hotmail.com"
    msg['Subject'] = "New Jeans on sale"
    s = smtplib.SMTP("smtp.live.com",587)
    html = open('new.html').read()
    parts = MIMEText(html, 'html')
    msg.attach(parts)
    s.ehlo() # Hostname to send for this command defaults to the fully qualified domain name of the local host.
    s.starttls() #Puts connection to SMTP server in TLS mode
    s.login('ptp_is@hotmail.com', os.environ["email"])
    s.sendmail("ptp_is@hotmail.com","ptp_is@hotmail.com", msg.as_string())
    s.quit()

def main():
    print "starting"
    new = get_current_price()
    print "got prices"
    print(new)
    if os.path.isfile("current.html"):
        print "something is already present"
        old = open("current.html").read()
        print "read old file" + str(len(old)) + "items"
        write_emailfile(new['name'],new['color'],new['salePrices'],new['OrgPrices'],"new.html")
        new = open("new.html").read()
        print "read new file" + str(len(new)) + "items"
        if new != old:
            print "They don't match"
            if '#00FF00' in new:
                print "something is red"
                send_email()
            os.rename("new.html","current.html")
            print "sent email"
        if new == old:
            print "they match deleting new"
            os.remove("new.html")
    else:
        print "didn't find a starting file, writeing current"
        write_emailfile(new['name'],new['color'],new['salePrices'],new['OrgPrices'],"current.html")

if __name__ == '__main__':
    main()
