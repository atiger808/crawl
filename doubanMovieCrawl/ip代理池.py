# _*_ coding: utf-8 _*_
# @Time     : 2018/11/21 2:50
# @Author   : Ole211
# @Site     : 
# @File     : ip代理池.py    
# @Software : PyCharm

import requests, threading, datetime
from bs4 import BeautifulSoup as bs
from headers import getheaders
import time
import random

# 写入文档
def write(path, ip):
    with open(path, 'a', encoding='utf-8') as f:
        f.writelines(ip)
        f.write('\n')

# 清空文档
def truncatefile(path):
    with open(path, 'w', encoding='utf-8') as f:
        f.truncate()

# 读取文档
def read(path):
    with open(path, 'r', encoding='utf-8') as f:
        txt = []
        for s in f.readlines():
            txt.append(s.strip())
    return txt

# 装饰器，计算运行时间
def runtime(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        print('start time: {}'.format(time.strftime('%Y-%m-%d %H:%M:%S')))
        back = func(*args, **kwargs)
        end = time.time()
        print('end time: {}'.format(time.strftime('%Y-%m-%d %H:%M:%S')))
        print('run time: %.2f' % (end - start))
        return back
    return wrapper

# 计算时间差
def gettimediff(start, end):
    seconds = (end - start).seconds
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    diff = ('%02d:%02d:%02d' % (h, m, s))
    return diff

# 检查IP是否可用
def checkip(targeturl, ip):
    headers = getheaders()
    proxies = {'http': 'http://' + ip, 'https': 'https://' + ip}
    try:
        res = requests.get(targeturl, proxies=proxies, headers=headers, timeout=5)
        if res.status_code == 200:
            return True
        else:
            return False
    except:
        return False

# 获取代理ip
def findip(type_id, pagenum, targeturl, path):
    'http://www.cnblogs.com/TurboWay/'  # 验证ip有效性的指定url
    type_list = {'1': 'http://www.xicidaili.com/nt/',  # xicidaili国内普通代理
                 '2': 'http://www.xicidaili.com/nn/',  # xicidaili国内高匿代理
                 '3': 'http://www.xicidaili.com/wn/',  # xicidaili国内https代理
                 '4': 'http://www.xicidaili.com/wt/'}  # xicidaili国外http代理
    url = type_list[str(type_id)] + str(pagenum)
    headers = getheaders()
    html = requests.get(url, headers=headers, timeout=5).text
    soup = bs(html, 'html.parser')
    all = soup.findAll('tr', class_='odd')
    for i in all:
        t = i.findAll('td')
        ip = t[1].text + ':' + t[2].text
        is_avail = checkip(targeturl, ip)
        if is_avail == True:
            write(path, ip)
            print(ip)

# 多线程抓取入口
def getip(targeturl, path):
    truncatefile(path)
    threads = [threading.Thread(target=findip, args=(type_id + 1, pagenum + 1, targeturl, path)) for type_id in range(4)
               for pagenum in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    ips = read(path)
    print('一共爬取代理ip: %s个' % (len(ips)))


if __name__ == '__main__':
    path = 'd:/csv/ip.txt'
    targeturl = 'http://ditu.hz.house365.com/ditu'
    # getip(targeturl, path)

