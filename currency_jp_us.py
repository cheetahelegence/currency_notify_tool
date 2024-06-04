import requests
from bs4 import BeautifulSoup as bf
import pandas as pd
import datetime
import pymysql
import line_notify


#爬蟲
bankURL = "https://rate.bot.com.tw/xrt?Lang=zh-TW"
response = requests.get(bankURL)
soup = bf(response.text, 'lxml')


#日圓現金/即期匯率
jp_cash = soup.find('tbody').find_all('tr')[7].find_all("td", "rate-content-cash text-right print_hide")
jp_sight = soup.find('tbody').find_all('tr')[7].find_all("td", "rate-content-sight text-right print_hide")
jp_threshold = jp_sight[0].text.strip()

jp_cash_buy = jp_cash[0].text.strip() #要用float嗎？
jp_cash_sale = jp_cash[1].text.strip()
jp_sight_buy = jp_sight[0].text.strip()
jp_sight_sale= jp_sight[1].text.strip()


#將資料放入DataFrame + 抓當日日期
col = ['現金買入', '現金賣出', '即期買入', '即期賣出']
jp_table = pd.DataFrame([jp_cash_buy, jp_cash_sale, jp_sight_buy, jp_sight_sale],index=col).T
#print(jp_table.iloc[0,1])
today = datetime.date.today()


#將資料匯入資料庫
try:
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='annroot0423',
                           database='currency_history',
                           port=3306,
                           charset='utf8')
    cursor = conn.cursor()
    try:
        sql = '''INSERT INTO yen1 (date, cash_buy, cash_sale, sight_buy, sight_sale)
                    VALUES (%s, %s, %s, %s, %s)'''
        var = (today, jp_table.iloc[0,0], jp_table.iloc[0,1], jp_table.iloc[0,2], jp_table.iloc[0,3])
        cursor.execute(sql, var)
        conn.commit()
        
    except Exception as e:
            print("錯誤訊息：", e)
except Exception as e:
        print("資料庫連接失敗：", e)
        
finally:
    conn.close()
    print("資料庫連線結束")
        

#設定提醒匯率金額
lowpoint = float(jp_sight_sale)
if lowpoint < 0.22:
    message = "\n%s的日圓\n即期買入為%s，即期賣出為%s\nhttp://127.0.0.1:5000/one" %(today, jp_sight_buy, jp_sight_sale)
    line_notify.notify(message)


    
    
















