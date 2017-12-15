import requests
from lxml import html

def get_current_shoes():
    url = 'http://www.merrell.com/US/en/outlet/?icid=navigation-header-sale#prefn1=bestFor&prefn2=genericSizeType&prefv3=Shoes&prefv4=10&prefv5=Waterproof&prefv6=M&prefv1=Hiking&prefv2=M&prefn3=productType&prefn4=size&prefn5=technologyCollection&prefn6=width'
    response = requests.get(url)
    print(response.status_code)
    index = 0
    report = []
    tree = html.fromstring(response.content)
    name = tree.xpath('//a[@class="name-link"]/text()')
    color = tree.xpath('//a[@class="product-swatches-all"]/text()')
    salePrices = tree.xpath('//span[@class="product-sales-price"]/text()')
    OrgPrices = tree.xpath('//span[@class="product-standard-price"]/text()')
    web_site_data = {"name":name, "color":color, "salePrices":salePrices, "OrgPrices":OrgPrices}
    while index < len(list['color']):
        data = {
            "name": list['name'][index],
            "color": list['color'][index],
            "salePrices" : list['salePrices'][index],
            "OrgPrices" : list['OrgPrices'][index]
        }
        if "Wide" not in data['name']:
            if "Women" not in data['name']:
                report.append(data)
        index = index + 1
    return report


def write_emailfile(current_shoes, filename):
    z = 0
    with open(filename,"a") as emailfile:
        emailfile.write("<html><head></head><body><table>")
        emailfile.write("<tr><th>Name</th><th>Color</th><th>Sale Price</th><th>Org Price</th></tr>")
        while z != len(current_shoes):
            if float(current_shoes[z].split("$")[1]) / float(current_shoes[z].split("$")[1]) < .50:
                emailfile.write("<tr bgcolor='#FF0000'>")
            elif float(current_shoes[z].split("$")[1]) / float(current_shoes[z].split("$")[1]) < .70:
                emailfile.write("<tr bgcolor='#FFFF00'>")
            elif float(current_shoes[z].split("$")[1]) / float(current_shoes[z].split("$")[1]) < .75:
                emailfile.write("<tr bgcolor='#00FF00'>")
            else:
                emailfile.write("<tr>")
            emailfile.write("<td>")
            emailfile.write(current_shoes['name'][z])
            emailfile.write("</td>")
            emailfile.write("<td>")
            emailfile.write(current_shoes['color'][z])
            emailfile.write("</td>")
            emailfile.write("<td>")
            emailfile.write(current_shoes['salePrices'][z])
            emailfile.write("</td>")
            emailfile.write("<td>")
            emailfile.write(current_shoes['OrgPrices'][z])
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
    print("starting")
    current_shoes = get_current_shoes()
    print("got current prices")
    if os.path.isfile("current.html"):
        print "something is already present"
        old = open("current.html").read()
        print "read old file" + str(len(old)) + "items"
        write_emailfile(current_shoes,"new.html")
        new = open("new.html").read()
        print "read new file" + str(len(old)) + "items"
        if new != old:
            print "They don't match"
            send_email()
            os.rename("new.html","current.html")
            print "sent email"
        if new == old:
            print "they match deleting new"
            os.remove("new.html")
    else:
        print "didn't find a starting file, writeing current"
        write_emailfile(current_shoes,"current.html")




if __name__ == __main__:
    main()
