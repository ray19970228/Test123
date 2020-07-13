import pandas as pd
import numpy as np 
#中壢
df1 = pd.read_csv("D:\\Data\\105Jongli_table1.csv",encoding = "big5", index_col= 0)
print(df1)
df2 = pd.read_csv("D:\\Data\\105Jongli_table2.csv",encoding = "big5", index_col= 0)
df3 = pd.read_csv("D:\\Data\\105Jongli_target_variable.csv",encoding = "big5", index_col= 0)

#桃園
df4 = pd.read_csv("D:\\Data\\105Taoyuan_table1.csv",encoding = "big5", index_col= 0)
df5 = pd.read_csv("D:\\Data\\105Taoyuan_table2.csv",encoding = "big5", index_col= 0)
df6 = pd.read_csv("D:\\Data\\105Taoyuan_target_variable.csv",encoding = "big5", index_col= 0)
#合併中壢資料
dfmerge1=pd.merge(df1,df2)
dfmerge2=pd.merge(dfmerge1,df3)
#print(dfmerge2)

#合併桃園資料
dfmerge3=pd.merge(df4,df5)
dfmerge4=pd.merge(dfmerge3,df6)
#用row合併中壢桃園資料
df=pd.concat([dfmerge2,dfmerge4],axis=0,sort=False)# axis=0 為直向合併
#所有含#_*及na替換成0
#df.to_csv('merge1.csv', header='column_names', encoding='big5')#read_csv() 讀取CSV文件的內容並返回DataFrame，to_csv() 則是其逆過程。
df = df.replace(".*(\#|\*|x|NA|NR|NaN)", "0",regex=True)#regex正規化
df= df.fillna(0)
#df.to_csv('merge2.csv', header='column_names', encoding='big5')



#Q1:請問105年SO2最大為多少
so2=df['SO2'].tolist()
result_so2=list(map(float,so2))
print('Q1: 105 年 SO2 最大值為',max(result_so2))

#Q2:105年中壢地區的平均一氧化碳 (CO) 濃度為多少
jongli_co=df[df["location"]=="中壢"]
co=jongli_co["CO"].tolist()
result_co=list(map(float,co))
print("Q2:中壢平均CO濃度",np.mean(result_co))

#Q3:請問 105 年 PM2.5 最高是發生在哪一天的哪一區域？
PM=df["PM2.5"].tolist()
result_PM=list(map(float,PM))
max=int(max(result_PM))
#max=str(max)
PM=df[df["PM2.5"]=="96"]
location_PM=PM["location"].tolist()
date_PM=PM["date"].tolist()
print("Q3:請問 105 年 PM2.5 最高是發生在哪一天的哪一區域？",date_PM,location_PM)


#Q4:請問 105 年 4 月桃園地區的平均臭氧 (O3) 濃度為多少？
C=df[df["location"]=="桃園"]
A=C.copy()
A["date"] = pd.to_datetime(A["date"]) #將資料型別轉換為日期型別
A=A.set_index("date") # 將date設定為index
B=A["2016-4"]
B=B["O3"].tolist()
result_B=list(map(float,B))
print("Q4: 105 4 月桃園地區的平均臭氧濃度為",np.mean(result_B))

#Q5:請問 105 年中壢和桃園地區的空汙資料中，與 PM2.5 相關係數超過 0.3 的汙染源有哪些？

a=df.columns
for i in range(len(a)):#把data,location,time去掉
    if a[i]!="date":
        if a[i]!="location":
            if a[i]!="time":
                df[a[i]]=df[a[i]].astype(float)
              
a=df.corr()#求算相關係數
a.sort_values(['PM2.5'], inplace = True)#inplace	是否用排序後的數據集替換原來的數據，默認爲False，即不替換
c = a[a['PM2.5'] > 0.3]
sta=c["PM2.5"].index[0:-1]
print('Q5: 105 年中壢和桃園地區的空汙資料中，與 PM2.5 相關係數超過 0.3 的汙染源有')
for i in range(len(sta)):
    print(c["PM2.5"].index[i])

#Q6:請列出一氧化氮(NO)低於其平均值中 PM10 濃度前十名的日期、時間，以及地點。
NO=df["NO"].tolist()
result_NO=list(map(float,NO))
Avg_NO=np.average(result_NO)
less_avg_no=df[df["NO"]<Avg_NO]#先算no小於平均值的部分
less_no=less_avg_no.copy()
less_no.sort_values(["PM10"],inplace=True,ascending=False)#遞減
rank=less_no["PM10"].tolist()
date=less_no["date"].tolist()
time=less_no["time"].tolist()
location=less_no["location"].tolist()
NO_rank=0
print("Q6:")
for i in range(len(rank)):
    if i>10:
        break
    else:
        NO_rank=NO_rank+1
        print('PM10 濃度:',rank[i],'第',NO_rank,'名','; 日期:',date[i],'; 時間:',time[i],';地點:',location[i])
        








