import requests
import json
from lxml import html

def get_ajm():
    AJM = 'https://www.ajmadison.com/cgi-bin/ajmadison/NV51K6650SS.html'
    response = requests.get(AJM)
    return response.text.split('"price_in_cart_signed_in":')[1][:4]

def get_hd():
    HD = 'https://www.homedepot.com/p/Samsung-30-in-Single-Electric-Wall-Oven-Self-Cleaning-with-Dual-Convection-in-Stainless-NV51K6650SS/300359599'
    page = requests.get(HD)
    tree = html.fromstring(page.content)
    HD_price = tree.xpath('//span[@class="price__dollars"]/text()')
    return HD_price

def get_sears():
    sears = 'http://www.sears.com/samsung-nv51k6650ss-aa-5.1-cu-ft-single-wall-oven/p-02229913000P'
    page = requests.get(sears)
    tree = html.fromstring(page.content)
    sears_price = tree.xpath('//span[@class="price-wrapper"]/text()')[0]
    return sears_price

def get_frys():
    fry ='https://www.frys.com/product/9128838'
    page = requests.get(fry)
    return page.content.split('<label id="l_price1_value_9128838" class="">')[1][:6]
