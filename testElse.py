
# def getConnection():
#     conn=pymysql.connect(host='localhost',user='root',password='123456',db='test',charset='utf8')
#     cursor=conn.cursor()
#     return conn,cursor

# conn,cursor=getConnection()
# sql=f"select * from `boat`"
# cursor.execute(sql)
# Boats=cursor.fetchall()
# print(Boats[1])
# print(Boats[1][0])
# cursor.close()
# conn.close()

# nameID=eval("1001")
# print(type(nameID))

# from partition import logReg
# print(logReg.judgeIdentity("admin"))


# from partition import statistics

# def addInfo():
#     conn,cursor=statistics.getConnection()
#     date=statistics.dateToday()
#     sql=f"insert into `info` values ('{date}','ALL',0,0,0,0)"
#     cursor.execute(sql)
#     conn.commit()
#     sql=f"insert into `info` values ('{date}','AM',0,0,0,0)"
#     cursor.execute(sql)
#     conn.commit()
#     sql=f"insert into `info` values ('{date}','PM',0,0,0,0)"
#     cursor.execute(sql)
#     conn.commit()
#     cursor.close()
#     conn.close()


# addInfo()

# 租船计时
# import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
# def Convert(t):
# 	# D = t % 10
# 	# 十位
# 	B = (t // 100) % 6
# 	# 个位
# 	C = (t // 10) % 10
# 	# 分钟
# 	A = t // 600
# 	return str(A) + ':' + str(B) + str(C)


# '''
# Function:
# 	开始计时
# '''
# def Start():
# 	global timer, color
# 	color = 'white'
# 	if not timer.is_running():
# 		timer.start()


# '''
# Function:
# 	停止计时
# '''
# def Stop():
# 	global timer, color
# 	timer.stop()
# 	color = 'white'


# '''
# Function:
# 	清空
# '''
# def Clear():
# 	global t, timer, color
# 	timer.stop()
# 	t = 0
# 	color = 'white'


# '''
# Function:
# 	计时器
# '''
# def timerHandler():
# 	global t
# 	t += 1


# '''
# Function:
# 	绘制时间
# '''
# def drawHandler(canvas):
# 	t_convert = Convert(t)
# 	canvas.draw_text(t_convert, (20, 120), 60, color, 'serif')


# '''
# Function:
# 	主函数
# '''
# def run():
# 	global t, color
# 	t = 0
# 	color = 'white'
# 	frame = simplegui.create_frame('Timer', 200, 200, 150)
# 	# 1000 / 100 = 10, 即t自加10次为一秒
# 	global timer
# 	timer = simplegui.create_timer(100, timerHandler)
# 	frame.set_draw_handler(drawHandler)
# 	button_start = frame.add_button('Start', Start, 150)
# 	button_stop = frame.add_button('Stop', Stop, 150)
# 	button_clear = frame.add_button('Clear', Clear, 150)
# 	frame.start()


# if __name__ == '__main__':
# 	run()


# from flask import Flask
# import datetime
# from flask_apscheduler import APScheduler

# aps = APScheduler()


# class Config(object):
#     JOBS = [
#         {
#             'id': 'job1',
#             'func': 'scheduler:task',
#             'args': (1, 2),
#             'trigger': 'interval',
#             'seconds': 10
#         }
#     ]
#     SCHEDULER_API_ENABLED = True


# def task(a, b):
#     print(str(datetime.datetime.now()) + ' execute task ' + '{}+{}={}'.format(a, b, a + b))


# if __name__ == '__main__':
#     app = Flask(__name__)
#     app.config.from_object(Config())

#     scheduler = APScheduler()
#     scheduler.init_app(app)
#     scheduler.start()

#     app.run(port=8000)


# import time
# from queue import Empty
# from telnetlib import STATUS
# from flask import (
#     Flask, render_template, request, redirect, url_for, globals, g)
# from partition import logReg
# from partition import statistics
# from partition import searchBoats

# from apscheduler.schedulers.blocking import BlockingScheduler
# from datetime import datetime

# globals.count = 0


# def my_block():
#     print("Hello! Can you hear me?")
#     globals.count = globals.count+1
#     if(globals.count == 2):
#         return
#     print(globals.count)
#     return 1

# if __name__ == '__main__':
# 	scheduler = BlockingScheduler()
# 	scheduler.add_job(my_block, 'interval', seconds=6)
# 	if globals.count == 2:
# 		scheduler.remove_job('my_block')
# 	scheduler.start()

# import datetime
# temp="2022-09-24"
# temp1="2022-09-24"
# print(temp!=temp1)

# boat=[{'id': 1, 'type': 'A', 'status': 0, 'totalT': 0.0, 'avgT': 0.0, 'maxT': 0.0, 'Time': 0, 'AP': 'AM'}, {'id': 1, 'type': 'A', 'status': 0, 'totalT': 87.7666, 'avgT': 21.9417, 'maxT': 74.9, 'Time': 4, 'AP': 'PM'}]
# for b in boat:
#     b['status']=2
# print(boat)

# print("0"+"2:17:00")
# print("2:17:35">"12:00:00")
# print("12:17:35">"12:00:00")

# from decimal import Decimal
# num=float(Decimal(2.333).quantize(Decimal('0.000')))
# print(num)
# from random import randint
# print(randint(1,22))
# li=[1,2,2,2,23]
# li1=[1,2,2,2,24]
# # print(li+li1)
# # li.extend(li1)
# # li=li+li1
# # print(li)
# print(set(li))

# x = [1,2,1,1,3,1,4,1,5,1,6,1,1,6]
# for i in range (x.count(1)):
#     x.remove(1)
#  # 有问题
# print(x)

# i x[0]=1
# i x[1]=1
# i x[2]=3
# i x[3]=1
# i x[4]=1