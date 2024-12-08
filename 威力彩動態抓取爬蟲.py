import selenium as sl
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import numpy as np
import time

slst = []

url = "https://www.taiwanlottery.com.tw/lotto/superlotto638/history.aspx"

driver = sl.webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(6)


year = [105,107,109]
# 模擬操作輸入欄位並點集查詢查找資料 再根據要抓取的屬性作抓取
for i in year:
    target = driver.find_element(By.ID,"SuperLotto638Control_history1_txtNO")
    target.clear() # 先清空在放新的值
    target.send_keys(str(i)+"000010")

    driver.find_element(By.ID,"SuperLotto638Control_history1_btnSubmit").click()
    #抓頁面
    html = driver.page_source
    soup = bs(html,"lxml")
    
    for n in range(1,8):
        temp = soup.find("span",{"id":"SuperLotto638Control_history1_dlQuery_SNo"+str(n)+"_0"})
        slst.append(int(temp.text))

    time.sleep(3)

    
res = np.array(slst).reshape(3,-1)

for i in range(3):
    print(f"{year[i]}第十期號碼: {res[i]}")

driver.quit()