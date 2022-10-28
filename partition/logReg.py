import pymysql
import requests as req
import time as t
import math
import random

def tempUser():
    User={"id":"","name":"","gender":"","tele":"","times":0,"pw":"","locked":0}
    infoU=["id","name","gender","tele","times","pw","locked"]
    return User,infoU

# 连接数据库
def getConnection():
    conn=pymysql.connect(host='localhost',user='root',password='123456',db='test',charset='utf8')
    cursor=conn.cursor()
    return conn,cursor

# 登录
def login():
    nameID=input("请输入用户名：")
    pw=input("请输入密码：")
    conn,cursor=getConnection()
    sql=f"select pw from `client` where `id`='{nameID}' or `name`='{nameID}'"
    cursor.execute(sql)
    
    try:
        realpw=cursor.fetchall()[0][0]
        for i in range(0,5):
            if str(realpw)==pw:
                print("登录成功！")
                userInfo(nameID)
                judgeIdentity(nameID)
                break
            else:
                pw=input("密码错误！请重新输入：")
                if i == 4:
                    print("密码错误次数过多！请稍后登录！")
    except:
        print("没有此用户！")

    cursor.close()
    conn.close()

# 获取用户信息
def userInfo(nameID,User=tempUser()[0],infoU=tempUser()[1]):
    conn,cursor=getConnection()
    sql=f"select * from `client` where id = '{nameID}' or name = '{nameID}'"
    cursor.execute(sql)
    detail=cursor.fetchall()
    print(detail)
    for i in range(0,7):
        print(detail[0][i])
        User[infoU[i]]=detail[0][i]
    # return User["name"] 
    return User  

# 获取用户信息--locked状态
def userLocked(nameID):
    conn,cursor=getConnection()
    sql=f"select locked from `client` where id = '{nameID}' or name = '{nameID}'"
    cursor.execute(sql)
    detail=cursor.fetchall()
    return detail[0][0]

    
# 注册    
def register(name,pw,pw2,gender,tele):
    
    # name=input("请输入用户名：")
    # pw=input("请输入密码：")
    # pw2=input("请再次输入密码：")
    # gender=input("请输入性别：")
    # tele=input("请输入电话号码：")
    id = random.randint(1000000000,9999999999)
    
    #验证两次密码是否一致
    while pw!=pw2:
        print("两次密码不一致！请重新输入！")
        pw2=input("请输入密码：")
    conn,cursor=getConnection()
    sql=f"insert into `client` values('{id}','{name}','{gender}','{tele}',0,'{pw}')"
    cursor.execute(sql)
    conn.commit()
    print("注册成功！请重新登陆！")                 #转去登录界面
    cursor.close()
    conn.close()

# 判断身份
def judgeIdentity(nameID):
    User=userInfo(nameID)
    if User['name']=="admin":
        # print("欢迎管理员")
        return 1
    else:
        # print("欢迎用户",nameID)
        return 0

# 修改名字
def modName(User=tempUser()[0]):
    name=input("输入用户名：")
    conn,cursor=getConnection()
    sql=f"update `client` set name='{name}' where id = '{User['id']}'"
    cursor.execute(sql)
    conn.commit()
    
    cursor.close()
    conn.close()

# 修改性别
def modGender(User=tempUser()[0]):
    gender=input("输入性别：")
    conn,cursor=getConnection()
    sql=f"update `client` set gender='{gender}' where id = '{User['id']}'"
    cursor.execute(sql)
    conn.commit()
    
    cursor.close()
    conn.close()

# 修改电话
def modTele(User=tempUser()[0]):
    tele=input("输入电话：")
    conn,cursor=getConnection()
    sql=f"update `client` set telephone='{tele}' where id = '{User['id']}'"
    cursor.execute(sql)
    conn.commit()
    
    cursor.close()
    conn.close()

# 修改密码
def modPw(User=tempUser()[0]):
    pw=input("输入密码：")
    conn,cursor=getConnection()
    sql=f"update `client` set pw='{pw}' where id = '{User['id']}'"
    cursor.execute(sql)
    conn.commit()
    
    cursor.close()
    conn.close()

# 核对信息
def matchPw(id,pw):
    pw=int(pw)
    conn,cursor=getConnection()
    sql=f"select pw from `client` where id = '{id}' or name = '{id}'"
    cursor.execute(sql)
    try:
        realpw=cursor.fetchall()[0][0]
        if realpw==pw:
            return True
        else:
            return False
    except:
        return False

# 测试code
# login()
# register()
# modName()
# modGender()
# modTele()
# modPw()
# print(matchPw(100001,"12345678"))

# print(userLocked(2200709193))
# print(userLocked("vsfbfv"))

# print(userInfo("vsfbfv"))