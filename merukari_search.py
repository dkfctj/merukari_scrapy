#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 15 22:40:33 2018

@author: jishuai
"""

from selenium import webdriver
import sys, pyperclip
from selenium.webdriver.common.by import By
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

if len(sys.argv) > 1:
    # get address from command line
    address = ''.join(sys.argv[1:])
else:
    address = pyperclip.paste()
 
Keywords = ['コスメデコルテ　フェイスパウダー','iphone']

browser = webdriver.Firefox()
browser.get('https://www.mercari.com/jp/search/?keyword='+Keywords[0]+'&status_on_sale=1')

#website format
#https://www.mercari.com/jp/search/?sort_order=&keyword=&category_root=&brand_name=&brand_id=&size_group=&price_min=&price_max=&status_on_sale=1


price_reg = browser.find_elements(By.XPATH, '//div[@class="items-box-price font-5"]')
price_link = browser.find_elements(By.XPATH,'//div[@class="items-box-content clearfix"]/section/a')
price_img = browser.find_elements(By.XPATH, '//div[@class="items-box-content clearfix"]/section/a/figure/img')


#/html/body/div/main/div[1]/section/div/section[1]/a
#/html/body/div/main/div[1]/section/div/section[2]/a
#/html/body/div/main/div[1]/section/div/section[1]/a/figure
#/html/body/div/main/div[1]/section/div/section[1]/a/figure/img


link = list()
for lk in price_link:
    link.append(lk.get_attribute('href'))



price = list()
for p in price_reg:
    price.append(p.text);

for i in range(len(price)):
    price[i] = price[i].replace('¥','')
    price[i] = price[i].replace(',','')
    price[i] = price[i].replace(' ','')

for i in range(len(price)):
    price[i] = int(price[i])
    
#save links of all images
image = list()
for img in price_img:
    image.append(img.get_attribute('data-src'))

#combine price with price link to a dictionary
#dic_price_link = dict(zip(price,link))
#dic_price_img = dict(zip(price,image))

browser.close()

server = smtplib.SMTP('smtp.gmail.com',587)

server.ehlo()
server.starttls()

#Next log in to the server
server.login("dkfctj@gmail.com", "ff512miy")


#Email content prepare
#Send embeded image
mail_content = ""

mail_title = "goods check"

#start using MIME function
msg = MIMEMultipart('related')
msg["Subject"] = Header(mail_title, 'utf-8')
msg["From"] = "dkfctj@gmail.com"
msg["To"] = Header("receiver", 'utf-8')  #the name of receiver can be defined here

msgAlternative = MIMEMultipart('alternative')
msg.attach(msgAlternative)


mail_body = []


i=0
# build the mail content 
for i in range(len(price)):
    if price[i] < 2300: 
        mail_body.append("""
            <p>hello, this is mail sending test </p>
            <p>Top 5 cheap list</p> 
            <a href="""+link[i]+""">"""+str(price[i])+"""</a>
            <p><img src="""+image[i]+"""></p>
            """)



mb_length = len(mail_body)
mail_body_comb = "<p>Qualified List</p>"
#combine each price content to a long string
for i in range(mb_length):
    mail_body_comb = mail_body_comb + str(i) + mail_body[i]
    
    

#msg.attach
msgText = (MIMEText(mail_body_comb, 'html', 'utf-8'))
msgAlternative.attach(msgText)

"""
#alocate graph path
img = open("try1.jpg", "rb")
msgImage = MIMEImage(img.read(), 'png')
img.close()

#define graph, id in HTML
msgImage.add_header('Content-ID','<send_image>')
msg.attach(msgImage)
"""



#msg = "why no output"
# Send the mail
#server.sendmail("dkfctj@gmail.com", "dkfctj@gmail.com", msg.as_string())
#server.sendmail("dkfctj@gmail.com", "wangxiaoli54321@yahoo.co.jp", msg)
server.sendmail("dkfctj@gmail.com", "wangxiaoli54321@yahoo.co.jp", msg.as_string())


server.quit()

