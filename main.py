import requests
import datetime
HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Linux; U; Mobile; Android 6.0.1;C107-9 Build/FRF91 )',
        'Referer': 'http://www.baidu.com',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh-TW;q=0.8,zh;q=0.6,en;q=0.4,ja;q=0.2',
        'cache-control': 'max-age=0'
}
url = 'http://jwgl.bupt.edu.cn/app.do'
session = requests.session()
user_id = ''


def login():
    while True:
        global user_id
        user_id = input("输入学号")
        user_pwd = input("输入密码")
        params = {
            'method': 'authUser',
            'xh': user_id,
            'pwd': user_pwd
        }
        req = session.get(url, params=params, headers=HEADERS, timeout=5)
        res = req.json()
        if not res['success']:  # 登录不成功
            print("登录不成功，请重试")
        else:
            break
    print("登录的用户为：")
    print(res['userrealname'] + ' ' + res['userdwmc'])
    HEADERS['token'] = res['token']


def get_time_info():
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    params = {
        'method': 'getCurrentTime',
        'currDate': current_date
    }
    req = session.get(url, params=params, headers=HEADERS)
    return req


def get_courses_info(zc=-1):
    time_info = get_time_info().json()
    params = {
        'method': 'getKbcxAzc',
        'xh': user_id,
        'zc': time_info['zc'] if zc == -1 else zc
    }
    req = session.get(url, params=params, headers=HEADERS)
    res = req.json()
    print(res)


def get_grades_info():
    time_info = get_time_info().json()
    params = {
        'method': 'getCjcx',
        'xh': user_id,
        'xqxnid': time_info['xnxqh']
    }
    req = session.get(url, params=params, headers=HEADERS)
    res = req.json()
    print("您本学期的各科成绩如下：")
    score_list = res['result']
    for i in score_list:
        print("%s 成绩：%s 学分：%s 考试类型：%s 课程类别：%s 课程性质：%s" % (i['kcmc'], i['zcj'], i['xf'], i['ksxzmc'], i['kclbmc'], i['kcxzmc']))


def get_exams_info():
    params = {
        'method': 'getKscx',
        'xh': user_id
    }
    req = session.get(url, params=params, headers=HEADERS)
    print(type(req.json()))
    res = req.json()
    print(res)


def get_empty_classrooms(idle_time='allday'):
    params = {
        'method': 'getKxJscx',
        'time': datetime.datetime.now().strftime("%Y-%m-%d"),
        'idleTime': idle_time
    }
    req = session.get(url, params=params, headers=HEADERS)
    res = req.json()
    classroom_list = res['data']
    print("当前时间段可用的教室有：")
    for i in classroom_list:
        print("位于%s的教室:" % i['jxl'])
        for j in i['jsList']:
            print("%s 座位数：%d 校区：%s" % (j['jsmc'], j['zws'], j['xqmc']))


def get_student_info():
    params = {
        'method': 'getUserInfo',
        'xh': user_id
    }
    req = session.get(url, params=params, headers=HEADERS)
    res = req.json()
    print("姓名：%s 学号：%s" % (res['xm'], res['xh']))
    print("班级：%s 学院：%s 专业名称：%s 年级：%s" % (res['bj'], res['yxmc'], res['zymc'], res['nj']))
    print("性别：%s 入学年份：%s" % (res['xb'], res['rxnf']))
    print("电话：%s email：%s" % (res['dh'], res['email']))


def main():
    login()
    while True:
        print('请输入以下命令对应的编号,输入“exit”退出：\n0.获取课程表\n1.获取当前学期成绩\n2.获取考试信息\n3.获取空教室信息\n4.获取学生信息')
        command_code = input()
        if command_code == '0':
            zc = input("请输入想要查询的周次，留空则查询当前周次：")
            if zc != '':
                get_courses_info(int(zc))
            else:
                get_courses_info()
        if command_code == '1':
            get_grades_info()
        if command_code == '2':
            get_exams_info()
        if command_code == '3':
            time_period = input("请输入想要查询的时间段，可选“allday”、“am”、“pm”、“night”、“xxyy”（表示从第xx节到yy节）,留空则为allday：")
            if time_period != '':
                get_empty_classrooms(time_period)
            else:
                get_empty_classrooms()
        if command_code == '4':
            get_student_info()
        if command_code == 'exit':
            exit(0)


if __name__ == '__main__':
    main()
