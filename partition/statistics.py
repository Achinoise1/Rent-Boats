from datetime import datetime
import pymysql
import requests as req
import time as t
import math
import random
import time

infoOne=["id","date","st","et","totalT","cid","ap"]

# 获取今天日期
def dateToday():
    return time.strftime("%Y-%m-%d", time.localtime())

# 连接数据库
def getConnection():
    conn=pymysql.connect(host='localhost',user='root',password='123456',db='test',charset='utf8')
    cursor=conn.cursor()
    return conn,cursor

# 计算avgT
def boatAvgT():
    
    conn,cursor=getConnection()
    sql=f"select totalT/time from `boat` as avgT"
    cursor.execute(sql)
    avgT=[]
    for c in cursor.fetchall():
        if c[0] is None:
            avgT.append(0)
        else:
            avgT.append(c[0])
    # print(avgT)
    
    sql=f"select id,AP from `boat` as maxT"
    cursor.execute(sql)
    idAP=list(cursor.fetchall())
    
    for i in range(0,len(idAP)):
        sql=f"update `boat` set avgT={avgT[i]} where id='{idAP[i][0]}' and AP='{idAP[i][1]}'"
        cursor.execute(sql)
        conn.commit()    
    
    cursor.close()
    conn.close()

# 计算totalT
def info(AP):

    date=dateToday()
    totalT=0
    conn,cursor=getConnection()
    if AP=="AM":
        sql=f"select totalT from `boat` where AP='AM'"
    elif AP=="PM":
        sql=f"select totalT from `boat` where AP='PM'"
    elif AP=="ALL":
        sql=f"select totalT from `boat`"
    cursor.execute(sql)
    tT=cursor.fetchall()
    
    for t in tT:
        totalT+=t[0]
     
    maxT=[]
    if AP=="AM":
        sql=f"select maxT from `boat` where AP='AM'"
    elif AP=="PM":
        sql=f"select maxT from `boat` where AP='PM'"
    elif AP=="ALL":
        sql=f"select maxT from `boat`"
    cursor.execute(sql)
    mT=cursor.fetchall()
    
    for t in mT:
        maxT.append(t[0])  
    temp=max(maxT)
    
    times=0
    if AP=="AM":
        sql=f"select Time from `boat` where AP='AM'"
    elif AP=="PM":
        sql=f"select Time from `boat` where AP='PM'"
    elif AP=="ALL":
        sql=f"select Time from `boat`"
    cursor.execute(sql)
    Ts=cursor.fetchall()
    
    
    for t in Ts:
        times+=t[0] 
    try:
        avgT=totalT/times
    except:
        avgT=0
        
    # sql=f"insert into `info`(totalT,maxT,avgT,time,type,date) values ('{totalT}','{temp}','{avgT}','{times}','{AP}','{date}')"
    sql=f"update `info` set totalT={totalT},maxT={temp},avgT={avgT},time={times} where type='{AP}' and date='{date}'"
    cursor.execute(sql)
    conn.commit()
    
    cursor.close()
    conn.close()

# 取出信息
def display(date):
    data=[]
    conn,cursor=getConnection()
    sql=f"select * from `info` where date='{date}'"
    cursor.execute(sql)
    for c in cursor.fetchall():
        data.append(c)    
    # print(data)
    # for d in data:
    #     print("Date:",d[0])
    #     print("Type:",d[1])
    #     print("Total Time:",d[2])
    #     print("Average Time:",d[3])
    #     print("Max Time:",d[4])
    #     print("Times:",d[5])
    #     print("")
        
    # 之后输出到网页可能会用到
    # print(str(data[12][0]))
    cursor.close()
    conn.close()
    return data

# 如果是首次登录需要清除数据
def clearInfo():
    
    conn,cursor=getConnection()
    sql=f"select date from `client` where id=100001"
    cursor.execute(sql)
    date=cursor.fetchall()[0]
    date=str(date[0])
    if date != dateToday():
        print(date != dateToday())
        print(date)
        print(dateToday())
        clearData()
        info("AM")
        info("PM")
        info("ALL")
        sql=f"update `client` set date='{dateToday()}' where id=100001"
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        return 1
    else:
        cursor.close()
        conn.close()
        return 0  
    
# 清除前一天的数据    
def clearData():
    
    conn,cursor=getConnection()
    sql=f"update `boat` set status=0,totalT=0,avgT=0,maxT=0,Time=0"
    cursor.execute(sql)
    conn.commit()
    
    cursor.close()
    conn.close()

# 如果当天还没有记录--则先新增记录
def addInfo():
    conn,cursor=getConnection()
    date=dateToday()
    sql=f"insert into `info` values ('{date}','ALL',0,0,0,0)"
    cursor.execute(sql)
    conn.commit()
    sql=f"insert into `info` values ('{date}','AM',0,0,0,0)"
    cursor.execute(sql)
    conn.commit()
    sql=f"insert into `info` values ('{date}','PM',0,0,0,0)"
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

# 取出records
def records(date):
    Records=[]
    conn,cursor=getConnection()
    sql=f"select * from `record` where date='{date}'"
    cursor.execute(sql)
    ars=cursor.fetchall()
    cursor.close()
    conn.close()
    total=len(ars)
    for j in range(0,len(ars)):
        temp={"id":"","date":"","st":"","et":"","totalT":"","cid":"","ap":""}
        for i in range(0,len(infoOne)):
            temp[infoOne[i]]=ars[j][i]
        Records.append(temp)
    return Records,total
    
# boatAvgT()

# info("AM")
# info("PM")
# info("ALL")

# display()

# clearInfo()