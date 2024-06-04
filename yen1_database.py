import csv
import pandas as pd
import pymysql

def organize_table(fn):
    file = fn
    with open(file, encoding='utf8') as csvFile:
        csvReader = csv.reader(csvFile)
        listReport = list(csvReader)
    currency_table=pd.DataFrame(i for i in listReport)
    currency_table.columns = currency_table.iloc[0]
    currency_table= currency_table[1:]
    delete_list=['幣別', "遠期10天", "遠期30天", "遠期60天", "遠期90天", "遠期120天", "遠期150天", "遠期180天"]
    currency_table=currency_table.drop(delete_list, axis=1)
    return currency_table

data1= organize_table('jpy/ExchangeRate@202305.csv')  
data2= organize_table('jpy/ExchangeRate@202306.csv')
data3= organize_table('jpy/ExchangeRate@202307.csv')
data4= organize_table('jpy/ExchangeRate@202308.csv')
data5= organize_table('jpy/ExchangeRate@202309.csv') 
data6= organize_table('jpy/ExchangeRate@202310.csv') 
data7= organize_table('jpy/ExchangeRate@202311.csv')  
data8= organize_table('jpy/ExchangeRate@20240524_202312.csv')



def add_to_database(data):
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='annroot0423',
                           database='currency_history',
                           port=3306,
                           charset='utf8')
    cursor = conn.cursor()
    for i in range(1,len(data)+1):
        sql = '''INSERT INTO yen1 (date, cash_buy, cash_sale, sight_buy, sight_sale)
                VALUES (%s, %s, %s, %s, %s)'''
        var = (data.iloc[-i,0], data.iloc[-i,2], data.iloc[-i,5], data.iloc[-i,3], data.iloc[-i,6])
        cursor.execute(sql, var)
    conn.commit()
    conn.close()

add_to_database(data1)
add_to_database(data2)
add_to_database(data3)
add_to_database(data4)
add_to_database(data5)
add_to_database(data6)
add_to_database(data7)
add_to_database(data8)



    
   

