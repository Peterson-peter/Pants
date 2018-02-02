#!/bin/python

import requests
from lxml import html
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os

AJM = 'https://www.ajmadison.com/cgi-bin/ajmadison/NV51K6650SS.html'
HD = 'https://www.homedepot.com/p/Samsung-30-in-Single-Electric-Wall-Oven-Self-Cleaning-with-Dual-Convection-in-Stainless-NV51K6650SS/300359599'
sears = 'http://www.sears.com/samsung-nv51k6650ss-aa-5.1-cu-ft-single-wall-oven/p-02229913000P'
fry ='https://www.frys.com/product/9128838'
BB = "https://www.bestbuy.com/site/samsung-30-single-wall-oven-stainless-steel/5581721.p?skuId=5581721"


def send_email():
    #msg = email.message_from_string()
    msg = MIMEMultipart('alternative')
    msg['From'] = "ptp_is@Hotmail.com"
    msg['To'] = "ptp_is@Hotmail.com"
    msg['Subject'] = "Oven Found on Sale"
    s = smtplib.SMTP("smtp.live.com",587)
    html = "<html><head></head><body><h3>Go look at ovens</h3><p><p> \
    <table><tr><th>Company</th><th>price</th><th>URL</th></tr> \
    <tr><td>ajmadison</td><td>"+str(get_ajm())+"</td><td>"+AJM+"</td></tr> \
    <tr><td>HomeDepot</td><td>"+str(get_hd())+"</td><td>"+HD+"</td></tr> \
    <tr><td>Sears</td><td>"+str(get_sears())+"</td><td>"+sears+"</td></tr> \
    <tr><td>Frys</td><td>"+str(get_frys())+"</td><td>"+fry+"</td></tr> \
    <tr><td>BestBuy</td><td>"+str(get_bb())+"</td><td>"+BB+"</td></tr> \
    </table></body></html>"
    parts = MIMEText(html, 'html')
    msg.attach(parts)
    s.ehlo() # Hostname to send for this command defaults to the fully qualified domain name of the local host.
    s.starttls() #Puts connection to SMTP server in TLS mode
    s.login('ptp_is@hotmail.com', os.environ["email"])
    s.sendmail("ptp_is@hotmail.com","ptp_is@hotmail.com", msg.as_string())
    s.quit()


def get_ajm():
    response = requests.get(AJM)
    print("Fetching AJM")
    return response.text.split('"price_in_cart_signed_in":')[1][:4].encode('ascii','replace')

def get_hd():
    page = requests.get(HD)
    tree = html.fromstring(page.content)
    print ("Fetching HD")
    HD_price = tree.xpath('//span[@class="price__dollars"]/text()')
    return HD_price[0]

def get_sears():
    page = requests.get(sears)
    tree = html.fromstring(page.content)
    print("Fetching Sears")
    sears_price = tree.xpath('//span[@class="price-wrapper"]/text()')[0][1:5]
    return sears_price

def get_frys():
    page = requests.get(fry)
    print("Fetching Frys")
    fprice = page.content.split('<label id="l_price1_value_9128838" class="">$')[1][:5].replace(",","")
    return fprice

def get_bb():
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(BB, headers=headers)
    print("Fetching Best Buy")
    return response.text.split('"currentPrice":')[1][:4].encode('ascii','replace')

def main():
    base = 1979
    prices = [get_ajm(), get_hd(), get_sears(), get_frys(), get_bb()]
    i=0
    while i < len(prices):
        print("found price: $" + prices[i])
        prices[i] = int(prices[i])
        if prices[i] < base:
            send_email()
            break
        i += 1


if __name__ == '__main__':
    main()
