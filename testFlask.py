import time
from queue import Empty
from telnetlib import STATUS
from flask import (
    Flask, render_template, request, redirect, url_for, globals)
from partition import logReg
from partition import statistics
from partition import searchBoats


search = Flask(__name__)


# 用来记录登录用户的信息--times可能需要另算
globals.User = {"id":"","name":"","gender":"","tele":"","pw":"","locked":0}
# login/reg--0|info--1
globals.status = 0
# 登录--0/注册--1
globals.condition = 0
# 登录时输入错误 0-wuwu|1--cuowu
globals.error = 0
# 注册时两次密码不匹配 0-匹配|1--不匹配
globals.retry = 0
# 未登录/普通用户|admin
globals.admin = 0
# 购买意向? 0-wu|1-you
globals.books = 0
# 是否有租借? 0-wu|1-you
globals.rent = 0
# 船只id
globals.boatID = 0
# 呼叫次数
globals.call = 0
# 是否被锁定
globals.locked = 0


# 首页   
@search.route('/', methods=['GET', 'POST'])
def index():
    # print(globals.User)
    statistics.clearInfo()
    if globals.call == 2:
        globals.locked=1
        searchBoats.lost(globals.User['id'],globals.boatID)
        globals.rent=0
    return render_template(
        "index.html",
        status=globals.status,
        admin=globals.admin,
        rent=globals.rent,
        id=globals.boatID
    )

# 个人主页信息
@search.route('/info', methods=['GET', 'POST'])
def info():
    # nameID=globals.User['id']
    # print(nameID)
    User=logReg.userInfo(globals.User['id'])
    globals.locked=User['locked']
    if User['locked'] == 1:
        acLocked="Locked"
    else:
        acLocked="Unlocked"
    return render_template(
        "info.html",
        ID=User["id"],
        name=User["name"],
        gender=User["gender"],
        tele=User["tele"],
        acLocked=acLocked,
        status=globals.status,
        admin=globals.admin,
        rent=globals.rent
    )

# 确认身份的中间路由函数
@search.route('/validation', methods=['GET', 'POST'])
def validation():
    nameID=request.form.get('nameID')
    pw=request.form.get('pw')
    
    # 输入的是id
    try: 
        if type(eval(nameID)==int):
            globals.User['id']=int(nameID)
    # 输入的是name
    except:
        globals.User['name']=str(nameID)
        
    # 成功匹配
    if logReg.matchPw(nameID,pw)==True:
        globals.status=1
        #是管理员
        if logReg.judgeIdentity(nameID)==1:
            globals.admin=1
        # 但是怎样赋值给books？
        # 如果是未登录时点击的book，登录之后跳回service页面
        if globals.books == 1:
            return render_template(
                "services.html",
                status=globals.status,
                admin=globals.admin,
                rent=globals.rent,
                id=globals.boatID
            )
        # 如果仅仅是未登录
        else:
            globals.locked=logReg.userLocked(nameID)
            return render_template(
                "index.html",
                status=globals.status,
                admin=globals.admin,
                rent=globals.rent,
                id=globals.boatID,
                locked=globals.locked
            )
    # 密码输错了
    else:
        globals.condition = 0
        globals.error = 1
        return render_template(
            "logreg.html",
            condition=globals.condition,
            error=globals.error                 
        )

# 登录
@search.route('/login', methods=['GET', 'POST'])
def login():
    globals.condition = 0
    globals.error = 0
    return render_template(
        "logreg.html",
        condition=globals.condition,
        error=globals.error
        )

# 输错密码的重新登陆
@search.route('/loginAgain', methods=['GET', 'POST'])
def loginAgain():
    globals.condition = 0
    globals.error = 1   
    return render_template(
        "logreg.html",
        condition=globals.condition,
        error=globals.error
        )

# 注册
@search.route('/register', methods=['GET', 'POST'])
def register():
    globals.condition = 1
    return render_template(
        "logreg.html",
        condition=globals.condition
        )

# 获取注册信息，如果两次密码匹配则讲信息存入数据库
@search.route('/registration', methods=['GET', 'POST'])
def registration():
    globals.User['name']=request.form.get('nameID')
    globals.User['pw']=request.form.get('pw')
    thePw=request.form.get('pw2')
    globals.User['tele']=request.form.get('tele')
    globals.User['gender']=request.form.get('gender')
    if thePw==globals.User['pw']:
        logReg.register(globals.User['name'],globals.User['pw'],thePw,globals.User['gender'],globals.User['tele'])
        globals.condition = 0
        globals.error = 0
        return render_template(
            "logreg.html",
            condition=globals.condition,
            error=globals.error
            )
    else:
        globals.retry = 1
        globals.condition = 1
        return render_template(
            "logreg.html",
            condition=globals.condition,
            retry=globals.retry
            )

# single改成statistics
# 船有可能是空的
@search.route('/statistics', methods=['GET', 'POST'])
def single():
    if statistics.clearInfo() == 0:
        statistics.info("AM")
        statistics.info("PM")
        statistics.info("ALL")
    date=statistics.dateToday()
    AllBoats=statistics.display(date)
    # print(AllBoats)
    # 如果还没有当日的记录，先进行insert
    if not AllBoats:
        statistics.addInfo()
    Boats=searchBoats.searchAllBoatsServer()
    Records,total = statistics.records(statistics.dateToday())
    return render_template(
        "statistics.html",
        date=date,
        AllBoats=AllBoats,
        Boats=Boats,
        admin=globals.admin,
        status=globals.status,
        rent=globals.rent,
        id=globals.boatID,
        Records=Records,
        total=total
        )

# 展示A/B type
@search.route('/service', methods=['GET', 'POST'])
def service():
    print(globals.locked)
    return render_template(
        "service.html",
        status=globals.status,
        admin=globals.admin,
        rent=globals.rent,
        id=globals.boatID,
        locked=globals.locked
        )

# 展示对应type下的船只
@search.route('/detailed/<string:type>', methods=['GET', 'POST'])
def detailed(type):
    AP=searchBoats.AMorPM(time.strftime("%H:%M:%S", time.localtime()))
    Boats=searchBoats.searchAllBoatsServer()
    print(Boats)
    return render_template(
        "detailed.html",
        AP=AP,
        Boats=Boats,
        status=globals.status,
        type=type,
        admin=globals.admin,
        rent=globals.rent,
        id=globals.boatID
    )

# 租赁船只界面展示
@search.route('/rent/<int:idx>', methods=['GET', 'POST'])
def rent(idx):
    if globals.rent == 0:
        searchBoats.rentBoats(globals.User['id'],idx+1)
        globals.rent=1
    globals.boatID=idx+1
    return render_template(
        "rent.html",
        id=idx+1,
        status=globals.status,
        admin=globals.admin,
        rent=globals.rent,
        call=globals.call
    )

# 租赁船只界面展示（呼叫版）
@search.route('/rent1/<int:idx>', methods=['GET', 'POST'])
def rent1(idx):
    globals.boatID=idx+1,
    globals.call=0
    return render_template(
        "rent.html",
        id=idx+1,
        status=globals.status,
        admin=globals.admin,
        rent=globals.rent,
        call=globals.call
    )

# 归还船只界面展示
@search.route('/return/<int:idx>', methods=['GET', 'POST'])
def returnBoat(idx):
    searchBoats.redelivery(globals.User['id'],idx+1)
    globals.rent=0
    return render_template(
        "returnBoat.html",
        status=globals.status,
        admin=globals.admin,
        id=idx+1,
        rent=globals.rent
    )

@search.route('/call1/<int:idx>', methods=['GET', 'POST'])
def call1(idx):
    globals.call=1
    return render_template(
        "call1.html",
        status=globals.status,
        admin=globals.admin,
        id=idx+1,
        rent=globals.rent,
        call=globals.call
    )

@search.route('/call2/<int:idx>', methods=['GET', 'POST'])
def call2(idx):
    globals.call=2
    return render_template(
        "call2.html",
        status=globals.status,
        admin=globals.admin,
        id=idx+1,
        rent=globals.rent,
        call=globals.call
    )

if __name__ == '__main__':
    search.run(debug=True)