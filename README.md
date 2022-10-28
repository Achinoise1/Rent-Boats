# Rent Boats
## templates 中的 html 模板
### call1.html       
 >第一次呼叫跳转到的界面  
 >显示一个 Can you hear me?  
### call2.html  
 >第二次呼叫跳转到的界面  
 >显示两个 Can you hear me?
### detailed.html    
 >A/B type下的船只(1-5/6-10)  
 >显示具体id船只的信息 在此处进行租赁
### index.html       
 >主界面(吉祥物)                 
### info.html
 >个人信息界面
### logreg.html
 >登录或者注册界面
### records.html
 >具体记录(仅admin可见)
### rent.html
 >租赁船只界面
### returnBoat.html
 >归还船只的界面  
 >自动跳转到index
### service.html
 >提供借船服务  
 >显示AB type，非具体id界面
### statistics.html
 >具体记录  
 >包含各个船只的单个记录和总记录和租赁条目

## static 存放图片和网页样式

## partition 存放py文件--处理信息的函数(后端的一部分)
### logReg.py -- 主要是登录等操作
### searchBoats.py -- 主要是租赁等操作
### statistics.py -- 数据展示部分
## testFlask.py
 >Flask框架  
 >路由函数连接前端和partition中的函数

## PS：其余文件对project运行影响不大，可删