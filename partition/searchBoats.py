import pymysql
import requests as req
import time as t
import math
import random
import datetime
import time

sum=10

infoBS=["id","type","status","totalT","avgT","maxT","Time","AP"]
infoBC=["id","type","status","AP"]
infoR=["id","date","st","et","totalT","cid"]

# 计算totalT
def totalT(st,et):
    return (et.seconds-st.seconds)/60               # 还船会用

# 获取当前日期
def dateToday():
    return time.strftime("%Y-%m-%d", time.localtime())

# 判断上下午
def AMorPM(temp):
    if temp > "12:00:00":
        return "PM"
    else:
        return "AM"

# 连接数据库
def getConnection():
    conn=pymysql.connect(host='localhost',user='root',password='123456',db='test',charset='utf8')
    cursor=conn.cursor()
    return conn,cursor

# 查找所有船
def searchAllBoatsServer():
    boat=[]
    conn,cursor=getConnection()
    sql=f"select * from `boat`"
    cursor.execute(sql)
    boats=cursor.fetchall()
    cursor.close()
    conn.close()
    for j in range(0,len(boats)):
        temp={"id":"","type":"","status":"","totalT":0,"avgT":0,"maxT":0,"Time":0,"AP":""}
        for i in range(0,len(infoBS)):
            temp[infoBS[i]]=boats[j][i]
        boat.append(temp)
    return boat 

# 查找所有船
def searchAllBoatsClient():
    boat=[]
    conn,cursor=getConnection()
    sql=f"select id,type,status,AP from `boat`"
    cursor.execute(sql)
    boats=cursor.fetchall()
    cursor.close()
    conn.close()
    for j in range(0,len(boats)):
        temp={"id":"","type":"","status":"","AP":""}
        for i in range(0,len(infoBC)):
            temp[infoBC[i]]=boats[j][i]
        boat.append(temp)
    return boat 

# 根据ID查找船
def searchBoatsById(id):
    boat=[]
    # id=input("请输入船的ID：")
    conn,cursor=getConnection()
    sql=f"select * from `boat` where id='{id}'"
    cursor.execute(sql)
    boats=cursor.fetchall()
    cursor.close()
    conn.close()
    for j in range(0,len(boats)):
        temp={"id":"","type":"","status":"","totalT":0,"avgT":0,"maxT":0,"Time":0,"AP":""}
        for i in range(0,len(infoBS)):
            temp[infoBS[i]]=boats[j][i]
        boat.append(temp)
    return boat

# 新增船
def addBoats():
    id=sum+1
    Type=input("请输入船的类型：")
    conn,cursor=getConnection()

    sql=f"insert into `boat` values('{id}','{Type}',0,0,0,0,0,'AM')"
    cursor.execute(sql)
    conn.commit()
    sql=f"insert into `boat` values('{id}','{Type}',0,0,0,0,0,'PM')"
    cursor.execute(sql)
    conn.commit()

# 查找剩余船只
def searchAllAvailableBoats():
    boats=searchAllBoatsClient()
    boat=[]
    for b in boats:
        if b["status"]==0 and b["AP"]==AMorPM(time.strftime("%H:%M:%S", time.localtime())):
            boat.append(b)
    return boat

# 租船
def rentBoats(cid,id):
# def rentBoats(cid):
    # boat=searchAllAvailableBoats()
    # if len(boat)==0:
    #     print("没有可用的船只")
    #     return
    # print("可用的船只有：")
    # for b in boat:
    #     print(b)
        
    # id=input("请输入船的ID：")
    st=time.strftime("%H:%M:%S", time.localtime())
    AP=AMorPM(st)
    Date=dateToday()
    
    # 数据库没改成功
    conn,cursor=getConnection()    
    sql=f"update `boat` set status=1 where id='{id}' and AP='{AP}'"
    cursor.execute(sql)
    conn.commit()
     
    sql=f"insert into `record` (Id,Date,St,Cid,AP) values ('{id}','{Date}','{st}','{cid}','{AP}')"
    cursor.execute(sql)
    conn.commit()
    
    sql=f"select times from`client` where id='{cid}'"
    cursor.execute(sql)
    times=cursor.fetchall()[0][0]
    # try:
    #     times=cursor.fetchall()[0][0]
    # except:
    #     times=0
    
    times=times+1
    sql=f"update `client` set times='{times}' where id='{cid}'"
    cursor.execute(sql)
    conn.commit()
    
    cursor.close()
    conn.close()

# 还船
def redelivery(cid,id):
    
    conn,cursor=getConnection()
    # id=input("请输入船的ID：")
    et=time.strftime("%H:%M:%S", time.localtime())
    
    # 获取借走船只的起始时间
    sql=f"select st from `record` where id='{id}' and Cid='{cid}' and et is null"
    cursor.execute(sql)
    st=cursor.fetchall()[0][0]
    print(st)
    AP=AMorPM("0"+str(st))
    print(AP)
    Date=dateToday()
    
    # 获取船只的总时间
    sql=f"select totalT,time from `boat` where id='{id}' and AP='{AP}'"
    cursor.execute(sql)
    try:
        tolT,times=cursor.fetchall()[0]
        times=times+1
        tolT=float(tolT)
    except:
        tolT,times=(0,0)
    
    
    # 处理船只结束时间
    et_split=et.split(":")
    et_final=datetime.timedelta(hours=int(et_split[0]),minutes=int(et_split[1]),seconds=int(et_split[2]))
    
    # 计算船只的租赁总时间
    tT=totalT(st,et_final)
    
    # 更新船只的租赁记录
    sql=f"update `record` set et='{et_final}',totalT='{tT}' where id='{id}' and cid='{cid}' and st='{st}' and et is null"
    cursor.execute(sql)
    conn.commit()
    
    # 获取船只的单次租赁最长时间
    sql=f"select maxT from `boat` where id='{id}' and AP='{AP}'"
    cursor.execute(sql)
    maxT=cursor.fetchall()[0][0]
    
    # 如果大于则进行更新
    if maxT<tT:
        maxT=tT
    
    # 更新船只的租赁总时间
    tolT=tolT+tT
    
    # 计算平均时间
    avgT=tolT/times
    
    # 更新到表格中
    sql=f"update `boat` set totalT='{tolT}',maxT='{tT}',avgT='{avgT}',status=0,time='{times}' where id='{id}' and AP='{AP}'"
    cursor.execute(sql)
    conn.commit()  
    
    cursor.close()
    conn.close()

# 查询记录
def searchRecords():
    record=[]
    conn,cursor=getConnection()
    sql=f"select * from `record`"
    cursor.execute(sql)
    records=cursor.fetchall()
    for r in records:
        temp={"id":"","st":"","et":"","totalT":0,"cid":""}
        for i in range(0,len(infoR)):
            temp[infoR[i]]=r[i]
        record.append(temp)    
    cursor.close()
    conn.close()
    return record

# 根据ID查询记录(输入的数字cid会转成字符串)
def searchIdvRec(cid):
    records=searchRecords()
    record=[]
    for r in records:
        if r["cid"]==str(cid):
            record.append(r)
    return record

# 丢失船只相关记录的更新
def lost(cid,id):
    # boat=searchBoatsById(id)
    # for b in boat:
    #     b['status']=2
    
    conn,cursor=getConnection()
    sql=f"update `boat` set status=2 where id='{id}'"
    cursor.execute(sql)
    conn.commit()
    
    sql=f"update `client` set locked=1 where id='{cid}'"
    cursor.execute(sql)
    conn.commit()
    
    date=dateToday()
    lostTime=time.strftime("%H:%M:%S", time.localtime())
    sql=f"insert into `lost` (Id,Cid,Date,Time) values ('{id}','{cid}','{date}','{lostTime}')"
    cursor.execute(sql)
    conn.commit()
    
    cursor.close()
    conn.close()
    


# 测试code
# print(searchAllBoats())
# print(searchAllBoatsServer())
# print(searchBoatsById())
# print(searchAllAvailableBoats())
# print(searchRecords())
# print(rentBoats(100001))
# print(searchIdvRec(100001))
# print(redelivery(100001))

# lost(2200709193,7)