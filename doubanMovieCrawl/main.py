# _*_ coding: utf-8 _*_
# @Time     : 2018/11/21 3:02
# @Author   : Ole211
# @Site     : 
# @File     : main.py
# @Software : PyCharm
# 爬取豆瓣电影信息
# 通过代理池，绕过豆瓣ip限制

from bs4 import BeautifulSoup as bs
from headers import getheaders
import requests
import time, datetime
import json
import random
import os

headers1 = {
    'Host': 'movie.douban.com',
    'Referer': 'https://movie.douban.com/explore'
}



# 计算运行时间装饰器
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

读取本地ip
def read():
    with open('d:/csv/ip.txt', 'r', encoding='utf-8') as f:
        txt = []
        for s in f.readlines():
            txt.append(s.strip())
    return txt

# 检验ip是否可用
def checkip(targeturl, ip):
    headers = getheaders()
    proxies = {'http': 'http://' + ip, 'https': 'https://' + ip}
    try:
        res = requests.get(targeturl, proxies=proxies, headers=headers)
        if res.status_code == 200:
            return True
        else:
            return False
    except:
        return False

# 页面解析
def parse(url):
    headers = getheaders()
    headers.update(headers1)
    ip_list = read()
    random.shuffle(ip_list)
    for ip in ip_list:
        try:
            if checkip(url, ip) == True:
                proxies = {'http': 'http://' + ip, 'https': 'https://' + ip}
                res = requests.get(url, proxies=proxies, headers=headers)
                if res.status_code == 200:
                    return res.text
                else:
                    return None
        except Exception as e:
            print(e)
            continue

# 保存为json文档
def save_json(dic, tag):
    if dic:
        with open(tag + '.json', 'a', encoding='utf-8') as f:
            content = json.dumps(dic, ensure_ascii=False) + '\n'
            f.write(content)

# 获取电影标签
def get_tags():
    tagUrl = 'https://movie.douban.com/j/search_tags?type=movie&source='
    res = parse(tagUrl)
    if res:
        return json.loads(res)['tags']
    return None

# 获取电影详情
def get_movie_info(movieUrl):
    html = parse(movieUrl)
    soup = bs(html, 'html.parser')
    li = soup.findAll('div', id='info')[0].text.strip().split('\n')
    li = [[i.split(':')[0].strip(), i.split(':')[1].strip()] for i in li]
    dic = {}
    for i in li:
        dic[i[0]] = i[1]
    return dic

# 单个页面下载入口
def load_one_page(url, tag):
    data = json.loads(parse(url))
    if data.get('subjects'):
        for i in data['subjects']:
            try:
                dic = {}
                for k, v in i.items():
                    dic[k] = v
                dic['info'] = get_movie_info(dic['url'])
                dic.update(dic['info'])
                save_json(dic, tag)
                print(dic['title'])
            except:
                continue

def main(offset, tag):
    limit = 20
    page_start = 20
    for i in range(offset):
        url = 'https://movie.douban.com/j/search_subjects?type=movie&tag={}&page_limit={}0&page_start={}'.format(tag, limit, page_start * i)
        load_one_page(url, tag)

# 主入口
@runtime
def enter():
    if not os.path.exists('d:/csv/豆瓣电影'):
        os.makedirs('d:/csv/豆瓣电影')
    os.chdir('d:/csv/豆瓣电影')
    tags = ['热门', '最新', '经典', '可播放', '豆瓣高分', '冷门佳片', '华语', '欧美', '韩国', '日本', '动作', '喜剧', '爱情', '科幻', '悬疑', '恐怖', '文艺']
    for tag in tags:
        main(10, tag)


if __name__ == '__main__':
    # enter()
