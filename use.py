import copy
import pickle
import datetime

with open("name_date_MA_df.pkl", "rb") as f2:
    name_date_MA_df = pickle.load(f2)
with open("name_price_dict_df.pkl", "rb") as f3:
    name_price_dict_df = pickle.load(f3)
with open("codename_list.pkl", "rb") as f4:
    codename_list = pickle.load(f4)
with open("sector_dict.pkl", "rb") as f5:
    sector_dict = pickle.load(f5)
#param_week_idx = 0
flat_list = []
ascending_list = []
descending_list = []

print("start here")
print(len(name_date_MA_df))

for stock in name_price_dict_df:
    name_price_dict_df[stock] = name_price_dict_df[stock].iloc[::-1, :].reset_index(drop=True)
    name_price_dict_df[stock].index.name = "order"
    name_price_dict_df[stock]['appraise'] = 'nan'

# name_price_dict_df['카카오뱅크']['appraise']='f'
"""
print(name_price_dict_df['카카오뱅크'])
print(name_price_dict_df['카카오뱅크'].loc[0])
print(type(name_price_dict_df['카카오뱅크'].loc[0]['30MA']))
print(name_price_dict_df['카카오뱅크'].loc[0]['30MA'])
"""
print(name_price_dict_df["AJ네트웍스"].iloc[0]["30MA"])
print(name_price_dict_df["AJ네트웍스"])

#모든 주식에 대해서 param_week_idx의 주의 30MA의 상/횡/하 상태를 name_date_MA_df에 넣는다.
def get_state(param_week_idx):
    returning_stock_state_list=[]
    for stock in name_date_MA_df:

        if param_week_idx>=len(name_date_MA_df[stock])+1:
            break;
        try:
            gradient = (name_date_MA_df[stock].iloc[param_week_idx]["30MA"] -
                        name_date_MA_df[stock].iloc[param_week_idx - 1]["30MA"]) / \
                       name_date_MA_df[stock].iloc[param_week_idx]["30MA"]
            if gradient>=0.003:
                returning_stock_state_list.append("a")
            elif gradient<=-0.003:
                returning_stock_state_list.append("d")
            else:
                returning_stock_state_list.append("f")

            if stock=="AJ네트웍스":
                print(gradient)

        except:
            print(stock+"excepted:"+str(i))
        #기준에 따라서 값 입력 영역

    return returning_stock_state_list

idx_statelist_dict={}
"""
for i in range(0,100):
    lis=get_state(i)
    if i==0 or i==1:
        print(len(lis))
    for j in range(len(lis)):
        try:
            idx_statelist_dict[j][i]=lis[j]
        except:
            idx_statelist_dict[j]=[0 for m in range(100)]
            idx_statelist_dict[j][i]=lis[j]

print(idx_statelist_dict[0])

name_date_MA_state_df=copy.deepcopy(name_date_MA_df)
i=0
for stock in name_date_MA_df:
    stock_datelength=len(name_date_MA_df[stock])
    name_date_MA_state_df[stock]["상태"]=idx_statelist_dict[i][:stock_datelength]
    i+=1

with open("name_date_MA_state_df.pkl","wb") as f1:
    pickle.dump(name_date_MA_state_df, f1)
print(name_date_MA_state_df["AJ네트웍스"].iloc[0:30])
"""
"""
sector_list=['종합(KOSPI)', '대형주', '중형주', '소형주', '음식료업', '섬유의복', '종이목재', '화학', '의약품', '비금속광물', '철강금속', '기계', '전기전자', '의료정밀', '운수장비', '유통업', '전기가스업', '건설업', '운수창고', '통신업', '금융업', '은행', '증권', '보험', '서비스업', '제조업']
#print(flat_list)
#print(ascending_list)
#print(descending_list)
print("end here")

for i in range(0,20):
    get_state(i)

print(name_date_MA_df)
"""


