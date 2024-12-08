# 自動化遊戲標題 JAVASCRIPT bs4抓不到
import selenium as sl
from selenium.webdriver.common.by import By
import time
url = "https://store.steampowered.com/charts/topselling/TW"

try:
    driver = sl.webdriver.Chrome()
    driver.maximize_window() # 視窗最大化
    driver.implicitly_wait(6) #開啟頁面時間
    time.sleep(6) # 抓取數據時間
    driver.get(url)
    # 容器型態
    lst = []
    # 找標題標籤
    title = driver.find_elements(By.CLASS_NAME,"weeklytopsellers_GameName_1n_4-")
    
    for i in title:
        lst.append(i.text)
except:
    print("資料抓取失敗!")
else:
    print("資料抓取成功!")
finally:
    driver.quit()
#%%
# 藉用request套件 將要傳的訊息po到line notify內 查看前五十名暢銷的即可
import requests as rq

def notify(msg,token):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization":"Bearer "+token}
    payload = {"message":msg}
    rq.post(url, headers = headers, data = payload)
    
token = "BG6dCybLbXxbTXEScCHD5DWTHuOYJvhEKQMyyUfnLfX" #自己的
for index, link in enumerate(lst[:50]): #將索引及資料分別帶出來
    msg = str(index+1) + link
    notify(msg, token)
print("line訊息已傳送完成!!")
#%%
import MySQLdb 
import pandas as pd

data = pd.DataFrame(lst,columns=["遊戲名"])
# print(data)

try:
    # 開啟資料庫連接
    conn = MySQLdb.connect(host="localhost",     # 主機名稱
                            user="root",        # 帳號
                            password="a22528680", # 密碼
                            database = "遊戲標題", #資料庫
                            port=3306,           # port
                            charset="utf8")      # 資料庫編碼
    
    # 使用cursor()方法操作資料庫
    cursor = conn.cursor()   
    # 將資料data寫到資料庫中
    try:
        
        for i in range(len(data)):
            sql = """INSERT INTO  STEAM暢銷遊戲資料 (遊戲名稱)
                                    VALUES (%s)"""
            var = data.iloc[i] 
            cursor.execute(sql, var)
            
        conn.commit()
        print("資料寫入完成")
        
    except Exception as e:
        print("錯誤訊息：", e)
 
except Exception as e:
    print("資料庫連接失敗：", e)
    
finally:
    conn.close()
    print("資料庫連線結束")