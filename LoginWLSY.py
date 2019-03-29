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
    response = session.post(url, fromData)
    
    # 判断登录状态
    soup = BeautifulSoup(response.text,'html.parser')
    if soup.title.string == '物理实验网络选课系统':

        # 获取学生姓名
        name = soup.find_all('span', id='Stu')[0].string.split('（')[0]
        
        # 抓取课表成绩页面
        response = session.get('http://wlsy.xidian.edu.cn/PhyEws/student/select.aspx')

        # 写入index.html
        # fp = open('index.html','w',encoding='utf-8')
        # fp.write(response.text)
        # fp.close()

        # 解析html页面
        soup = BeautifulSoup(response.text,'html.parser')

        # 获取表头
        th = soup.find_all('th', class_='tableHeaderText')
        head=[]
        for item in th:
            head.append(item.string)
        
        # 获取表格内容
        td = soup.find_all('td', class_='forumRow')
        body = []
        for item in td:
            body.append(item.string)
        body = [body[i:i+10] for i in range(0, len(body), 10)]

        # 判断是否需要下载课件
        downStatus = []
        for item in body:
            if item[6] == '下载':
                downStatus.append(True)
            else:
                downStatus.append(False)
        
        # 获取下载链接
        a = soup.find_all('a', class_='linkSmallBold')[1::2]
        downUrl = []
        for i in range(len(a)):
            if downStatus[i]:
                downUrl.append(a[i]['href'])
            else:
                downUrl.append(None)
        
        # 结果写入result.csv  open()中的编码方式请与本机默认编码保持一致
        fp = open('result.csv','w',encoding='gbk')
        for item in head:
            fp.write(item)
            fp.write(',')
        fp.write('\n')
        
        for i in body:
            for j in i:
                fp.write(str(j))
                fp.write(',')
            fp.write('\n')
        fp.close()
        
        return {
            'head': head,
            'body': body,
            'downStatus': downStatus,
            'downUrl': downUrl,
        }

    # 登录失败
    else:
        return {
            'result': 'failed',
            'reason': '登录失败，请检查学号或密码是否正确'
        }

if __name__ == '__main__':
    print(main())
