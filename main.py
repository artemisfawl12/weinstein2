import csv
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
import requests
import pickle
from bs4 import BeautifulSoup
def get_code(df, name):
    code = df.query("name=='{}'".format(name))['code'].to_string(index=False)

f1=open('C:\\sectordata\\kospi_1.txt','r')
codename_list=[]
i=0
for line in f1:
    if i!=0:
        line_=''.join(line.split(' '))
        line_list=line_.split()
        code=line_list[0].zfill(6)
        name=line_list[2]
        name=name.split("\n")[0]
        codename_list.append([code,name])
    i+=1

#print(codename_list)
print(len(codename_list))

sector_dict={}
for j in range(1,28):
    sector_list_frag=[]
    if 0<j<10:
        fmt="00"+str(j)+"codelist.txt"
    if 10<=j:
        fmt = "0" + str(j) + "codelist.txt"
    if j!=23:
        f2=open('C:\\sectordata\\'+fmt,'r')

        i=0
        for line in f2:
            if i != 0:
                code = line[0:6]
                name = line[11:]
                name = name.split("\n")[0]
                sector_list_frag.append([code, name])

            i += 1
        sector_dict[j]=sector_list_frag

#print(sector_dict)
print(codename_list)
#여기까지 업종별 분류 완료. j=23인 업종제외하고는 모두 업종이 있다. 그래서 총 26개 업종
#이제 야후에서 받아와서 차트로 만들고 딥러닝에 넣자.

#['종합(KOSPI)', '대형주', '중형주', '소형주', '음식료업', '섬유의복', '종이목재', '화학', '의약품', '비금속광물', '철강금속', '기계', '전기전자', '의료정밀', '운수장비', '유통업', '전기가스업', '건설업', '운수창고', '통신업', '금융업', '은행', '증권', '보험', '서비스업', '제조업']
a=0
name_price_dict={}

for code_name_pair in codename_list:
    data_list=[]
    if a>1000:
        break
    code=code_name_pair[0]
    url='http://fchart.stock.naver.com/sise.nhn?timeframe=week&count=200&requestType=0&symbol='+code

    price_data=requests.get(url)
    html=BeautifulSoup(price_data.text, "lxml")
    items_list=html.find_all('item')
    for item in items_list:
        data=item['data'].split('|')
        data_list.append(data)
    name_price_dict[code_name_pair[1]]=data_list
    a+=1
#print(name_price_dict)

name_price_dict_df={}
column_list=['날짜','시가','고가','저가','종가','거래량']
print(len(name_price_dict_df))
for stock in name_price_dict:
    stock_df=pd.DataFrame(name_price_dict[stock],columns=column_list)
    name_price_dict_df[stock]=stock_df


for stock in name_price_dict_df:
    name_price_dict_df[stock]["30MA"]=name_price_dict_df[stock]["종가"].rolling(window=30).mean()

print(len(name_price_dict_df))
name_date_MA_df={}
print(name_price_dict_df['AJ네트웍스'])
for stock in name_price_dict_df:
    Date_MA_df=name_price_dict_df[stock][["날짜","30MA","거래량","종가"]]
    Date_MA_df=Date_MA_df.iloc[::-1,:].reset_index(drop=True)
    Date_MA_df.index.name = "order"
    name_date_MA_df[stock]=Date_MA_df

print(name_date_MA_df['AJ네트웍스'])
#print(len(codename_list))
#etf 등등은 다 제거하고 코스피 실제 개별종목만 딱 남긴거같네요

with open("name_date_MA_df.pkl","wb") as f2:
    pickle.dump(name_date_MA_df, f2)
with open("name_price_dict_df.pkl","wb") as f3:
    pickle.dump(name_price_dict_df,f3)
with open("codename_list.pkl","wb") as f4:
    pickle.dump(codename_list,f4)
with open("sector_dict.pkl","wb") as f5:
    pickle.dump(sector_dict,f5)
#일단 MA가 일정 범위에 있는거까지 했으니까 다음번에는
#가격이 MA기준으로 어느 범위에 있는지, MA보다 윈지 아랜지 등등으로 단계 판단하는게 좋을듯
