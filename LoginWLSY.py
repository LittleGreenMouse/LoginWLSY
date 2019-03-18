import urllib.parse
import requests
from bs4 import BeautifulSoup

def main():
    # 输入学号密码
    stuId = input('stuId: ')
    password = input('password: ')

    # 登录地址
    url = 'http://wlsy.xidian.edu.cn/PhyEws/default.aspx?ReturnUrl=%2fPhyEws%2fstudent%2fstudent.aspx'
    # 构造登录所需数据
    fromData = {
        '__EVENTARGUMENT':'',
        '__EVENTTARGET':'',
        '__VIEWSTATE':'/wEPDwUKMTEzNzM0MjM0OWQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFD2xvZ2luMSRidG5Mb2dpbutGpJNAAaBhxseXkh1n/woLBppW',
        '__EVENTVALIDATION':'/wEWBwLsvJu+AgKckJOGDgKD8YXRCQLJ5dDDBAKVx8n1CQKytMi0AQKcg465CqDdcB40IuBzviNuzXl4xNRdD759',
        'login1$btnLogin.y':10,
        'login1$btnLogin.x':25,
        'login1$StuPassword':password,
        'login1$StuLoginID':stuId,
        '__VIEWSTATEGENERATOR':'EE008CD9',
        'login1$UserRole':'Student',
    }

    # 建立会话
    session = requests.session()
    session.post(url, fromData)
    # 抓取课表成绩页面
    response = session.get('http://wlsy.xidian.edu.cn/PhyEws/student/select.aspx')
    html = (response.text)

    # 写入index.html
    # fp = open('index.html','w',encoding='utf-8')
    # fp.write(html)
    # fp.close()

    # 解析html页面获取课表成绩信息
    soup = BeautifulSoup(html,'html.parser')
    table = str(soup.select("table#Table1"))
    soup = BeautifulSoup(table,'html.parser')
    tbody = str(soup.select("form#Form1"))
    soup = BeautifulSoup(tbody, 'html.parser')
    table2 = str(soup.select("table#Orders_ctl00"))
    soup = BeautifulSoup(table2, 'html.parser')
    th = soup.select("th.tableHeaderText")
    td = soup.select("td.forumRow")

    head = []
    body = []
    downState = []
    down = ['http://wlsy.xidian.edu.cn/pec/wenjian.asp?id=69',downState]

    for i in th:
        head.append(i.get_text())
    head[len(head)-1] = '页码'

    temp = []
    n = 0
    for j in td:
        n = n + 1
        temp.append(j.get_text())
        if(n == 7):
            if(j.get_text() == '下载'):
                downState.append(True)
            else :
                downState.append(False)
        if(n == 10):
            n = 0
            body.append(temp)
            temp = []

    ''' 
    最终结果：
    head    表头
    body    选课及成绩
    down[0] 新开实验讲义下载地址
    down[1] 是否为新开实验
    '''
    print(head)
    for i in body:
        print(i)
    print(down[0])
    print(down[1])

    # 结果写入result.csv  open()中的编码方式请与本机默认编码保持一致
    fp = open('result.csv','w',encoding='gbk')
    for i in head:
        fp.write(i)
        fp.write(',')
    fp.write('\n')

    for i in body:
        for j in i:
            fp.write(j)
            fp.write(',')
        fp.write('\n')


if __name__ == '__main__':
    main()