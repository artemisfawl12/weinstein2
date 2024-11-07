import copy
import pickle
import datetime

with open("name_date_MA_state_df.pkl", "rb") as f2:
    name_date_MA_state_df = pickle.load(f2)



def new_high_point(stock,param_weekcount):
    #20주 이하면 자른다.
    if len(name_date_MA_state_df[stock])<20:
        print("데이터가 20주 이하: "+stock)
    else:
        max_price = 0
        max_day = 0
        max_index = 0
        high_point_list_byindex=[]
        valuable_sorted_high_point_list_byindex=[]
        for i in range(len(name_date_MA_state_df[stock])-1,-1,-1):
            try:
                #print(float(name_date_MA_state_df[stock].iloc[i]["종가"]))
                if int(name_date_MA_state_df[stock].iloc[i]["종가"])>max_price:
                    max_price=int(name_date_MA_state_df[stock].iloc[i]["종가"])
                    max_index=i
                    max_day=name_date_MA_state_df[stock].iloc[i]["날짜"]
                    high_point_list_byindex.append(i)
            except:
                print(stock)

        #high_point_list_byindex에는 index 값이 들어갈때 큰거부터 작은거로 역순으로 들어간다. 시간상으로는 과거의 것이 먼저 들어가있다.

        for idx in range(len(high_point_list_byindex)-1):
            #high_point_list_byindex에 len(name_date_MA_state_df[stock])-1이 맨앞에 무조건 들어가므로 리스트의 최초값이 의미있는 신고가값일경우를 걱정할필요가 없다.
            if high_point_list_byindex[idx]-high_point_list_byindex[idx+1]>=param_weekcount:
                valuable_sorted_high_point_list_byindex.append(high_point_list_byindex[idx+1])
        #valuable_sorted_high_point_list_byindex에도 index는 큰것->작은것 순이다. 즉 과거->현재 순으로 나열되어있다.
        return valuable_sorted_high_point_list_byindex



whole_length=0
count_fly=0
count_ascending_and_fly=0
count_descending_and_fly=0
count_flat_and_fly=0
count_zero_and_fly=0
count_up=0
count_ascending_and_up=0
count_descending_and_up=0
count_die=0
count_ascending_and_die=0
count_descending_and_die=0
count_flat=0
#30주 MA의 상태가 a d f인지를 보는 기능도 추가.
for stock in name_date_MA_state_df:
    valuable_sorted_high_point_list_byindex=new_high_point(stock,10)
    for i in valuable_sorted_high_point_list_byindex:
        if i>2:
            #2주 후에 얼마나 올랐는지를 기준으로 count_fly에 넣는다 5%기준
            if int(name_date_MA_state_df[stock].iloc[i-2]["종가"])/int(name_date_MA_state_df[stock].iloc[i]["종가"]) *100>=125:
                count_fly+=1
                whole_length+=1
                percentage=(int(name_date_MA_state_df[stock].iloc[i-2]["종가"])/int(name_date_MA_state_df[stock].iloc[i]["종가"]) *100 -100)

                if name_date_MA_state_df[stock].iloc[i]["상태"]=="a":
                    count_ascending_and_fly+=1
                elif name_date_MA_state_df[stock].iloc[i]["상태"]=="d":
                    count_descending_and_fly+=1
                elif name_date_MA_state_df[stock].iloc[i]["상태"]=="f":
                    count_flat_and_fly+=1
                else:
                    count_zero_and_fly+=1
                    print(stock + ": " + str(i) + " || " + str(
                        int(name_date_MA_state_df[stock].iloc[i - 2]["종가"])) + " vs " + str(
                        int(name_date_MA_state_df[stock].iloc[i]["종가"])) + " || " + str(round(percentage, 1)))
                    print(str(len(name_date_MA_state_df[stock])-i))
            elif int(name_date_MA_state_df[stock].iloc[i-2]["종가"])/int(name_date_MA_state_df[stock].iloc[i]["종가"]) *100>=105:
                count_up+=1
                whole_length+=1
                if name_date_MA_state_df[stock].iloc[i]["상태"]=="a":
                    count_ascending_and_up+=1
                elif name_date_MA_state_df[stock].iloc[i]["상태"]=="d":
                    count_descending_and_up+=1
            elif int(name_date_MA_state_df[stock].iloc[i]["종가"])/int(name_date_MA_state_df[stock].iloc[i-2]["종가"]) *100>=105:
                count_die+=1
                whole_length+=1
                if name_date_MA_state_df[stock].iloc[i]["상태"]=="a":
                    count_ascending_and_die+=1
                elif name_date_MA_state_df[stock].iloc[i]["상태"]=="d":
                    count_descending_and_die+=1
            else:
                whole_length+=1
                count_flat+=1
                

print("whole: "+str(whole_length))
print("fly: "+str(count_fly))
print("up: "+str(count_up))
print("die: "+str(count_die))
print("flat: "+str(count_flat))

print("count_ascending_and_fly: "+str(count_ascending_and_fly))
print("count_descending_and_fly: "+str(count_descending_and_fly))
print("count_flat_and_fly: "+str(count_flat_and_fly))
print("count_zero_and_fly: "+str(count_zero_and_fly))
print("count_ascending_and_die: "+str(count_ascending_and_die))
print("count_descending_and_die: "+str(count_descending_and_die))
print("count_ascending_and_up: "+str(count_ascending_and_up))
print("count_descending_and_up: "+str(count_descending_and_up))

