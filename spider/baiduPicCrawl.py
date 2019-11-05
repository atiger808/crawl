# _*_ coding: utf-8 _*_
# @Time     : 2019/11/5 14:51
# @Author   : Ole211
# @Site     : 
# @File     : baiduPicCrawl.py    
# @Software : PyCharm

import re
import requests
import json
import time
import threading
import os, argparse
from run_time import run_time as run

# 运行爬虫， 命令行格式：
# python baiduPicCrawl.py -k '搜索关键词' -p 页数 -d 保存的文件夹名字（default=image）


header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.image; Win64; x64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'}

class myThreadPic(threading.Thread):
    def __init__(self, urllist, data_folder_name, non_repetitive_url, lock):
        super(myThreadPic, self).__init__()
        self.urllist = urllist
        self.data_folder_name = data_folder_name

        self.non_repetitive_url = non_repetitive_url
        self.lock = lock
    def run(self):
        global num
        for i in self.urllist:
            print('开始下载---------', num)
            if i not in self.non_repetitive_url:
                respl = requests.get(i).content
                with open(self.data_folder_name+r'/'+str(time.time())+'.jpg', mode='wb') as f:
                    f.write(respl)
                self.non_repetitive_url.add(i)
                self.lock.acquire()
                num += 1
                self.lock.release()

def baidu_pic_crawl(keyword, page, data_folder_name):
    non_repetitive_url = set()
    regr = r'''hoverURL":"(.*?)"'''
    pattern = re.compile(regr)
    url = '''https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&fp=result&queryWord=''' + keyword + '''&word=''' + keyword + '''&pn=%d&rn=%d&gsm=168'''
    urllist = [url%(i, 30) for i in range(0, 30*page, 30)]
    result = []
    lock = threading.Lock()
    for urli in urllist:
        try:
            resp = requests.get(urli, headers=header).text
            data = pattern.findall(resp)
            data = [i for i in data if len(i)>0]
            data = set(data)
            # 开启一个线程下载器
            pic_crawl = myThreadPic(data, data_folder_name, non_repetitive_url, lock)
            pic_crawl.start()
        except Exception as e:
            print(e)
            continue


def load_enter():
    global num
    # 命令行解析对象
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--keyword', type=str, help='搜索关键词：')
    parser.add_argument('-p', '--page', type=int, help='下载的页数')
    parser.add_argument('-d', '--data_folder_name', default='image', type=str, help='数据保存的文件夹')
    args = parser.parse_args()
    num = 0
    if not os.path.exists(args.data_folder_name):
        os.mkdir(args.data_folder_name)
    baidu_pic_crawl(args.keyword, args.page, args.data_folder_name)

if __name__ == '__main__':
    t0 = time.time()
    load_enter()
    print('waste time: %s'%(time.time() - t0) )
