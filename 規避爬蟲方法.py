# 進階爬蟲 表頭偽裝
import requests as rq

url = "https://www.momoshop.com.tw/main/Main.jsp"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}

r = rq.get(url,headers = headers)
if r.status_code == 200: # rq.codes.ok 就是 200
    r.encoding = "Big5"
    print(r.text)
else:
    print("網頁請求錯誤!")
#%% 設定cookie
import requests as rq
from bs4 import BeautifulSoup as bts
url = "https://www.ptt.cc/bbs/Tech_Job/index3999.html"
r = rq.get(url,cookies={"over18" :"1"})
if r.status_code == rq.codes.ok:
    html = bts(r.text,"lxml")
    # select 找div內.=class內title內的a
    data = html.select("div.title a") 
    for i in data:
        print(i.text)
else:
    print("請求出錯")
#%%
import requests as rq
from bs4 import BeautifulSoup as bts
url = "https://www.ptt.cc/bbs/Tech_Job/index.html"
r = rq.get(url)
if r.status_code == rq.codes.ok:
    html = bts(r.text,"html.parser")
    divs = html.find_all("div",{"class":"r-ent"})
    for div in divs:
        div_title = div.find_all("div",{"class":"title"})
        # for i in div_title:
        #     print(i.text)
    lst = []
    for div in div_title: 
        if div.find_all("a") != None:
            title = div.find("a").text
            lst.append(title)
    print(lst)
else:
    print("請求出錯")
#%%
from bs4 import BeautifulSoup as BS
import requests as rq
import re

res = rq.get("https://www.ptt.cc/bbs/Tech_Job/index.html")
html = BS(res.text,"html.parser")
divs = html.find_all("div", {"class": "r-ent"})



# for div in divs:
#     div_title = div.find("div", {"class": "title"})
#     if div_title.find("a") != None:
#         title = div.find("a").text
#         date = div.find("div", { "class": "date"}).text
#         print(title, date)
        
for div in divs:
    div_title = div.find('div',{'class':'title'})
    if div_title.find('a') != None:
        title = div_title.find('a').text
        date  = div.find('div',{'class':'date'}).text
        print(title,date)

            
#%% 更改proxy ip
from bs4 import BeautifulSoup as bs
import random as rd
import requests as rq
while True:
    try:
        proxy_ips = ["47.91.56.120:8081","138.68.60.8:3128"]
        ip = rd.choice(proxy_ips)
        print("Use: ",ip)
        url = "http://ip.filefab.com"
        r = rq.get(url)
        proxys = {"http":"http://"+ip}
        
        html = bs(r.text,"lxml")
        print(html.find("h1",id="ipd").text.strip())
        if ip == "ipd":
            break
    except:
        continue
#%%
import requests as rq
from bs4 import BeautifulSoup as bs

url = "https://news.google.com/home?hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
res = rq.get(url)

soup = bs(res.text,"lxml")
target = soup.select("h4.gPFEn")

lst = []
# for i in target:
#     print(i.text)

for i in target:
    lst.append(i.text)

# line notify
def notify(msg,token):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization":"Bearer "+token}
    payload = {"message":msg}
    rq.post(url, headers = headers, data = payload)
    
token = "c6TtNzsSDAEAeGrHpf1fNV5x4MGDCewFsH92AyzGT5b" #自己的
for index, link in enumerate(lst):
    msg = str(index+1)+". " + link
        
    notify(msg, token)