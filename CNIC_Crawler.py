# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 19:28:36 2017

@author: SY_GAO
"""

import requests
from bs4 import BeautifulSoup
import os
import re

def get_content(url_page, page_num):
    #print('新闻列表页'+ url_page)
    #------------------当前页面都有哪些新闻链接-----------------#
    if page_num:
        suffix = '/index_'+str(page_num)+'.html'
    else:
        suffix = '/index.html'
    url_get = requests.get(url_page+suffix)
    soup = BeautifulSoup(url_get.content.decode(), 'lxml')
    find_result = soup.find(id = 'content').find_all('li')
    #--------------------------------------------------------#
    url_target = []#每个页面新闻链接汇总，每条链接末尾字串
    for li in find_result:
        url_target.append(url_page + li.a.get('href')[1:])
    url_target_num = 0
    for url in url_target:
        print('新闻链接'+url)
        try:
            url_news = requests.get(url)
            soup = BeautifulSoup(url_news.content.decode(), 'lxml')
            #print(soup)
            title = soup.find_all('h2')[-1].get_text()
            content_list = soup.find('div', class_ = 'TRS_Editor').find_all('span')
            content = ''
            for c in content_list:
                content += c.get_text()
            news = title + '\n' + '\n' + content
            file_name = url_target[url_target_num] + '.txt'
            file_name = re.sub('/','_',file_name)
            file_name = re.sub(':','_',file_name)
            url_target_num += 1
            print(news)
            #news.encode('utf-8')
            f = open(file_name, 'w',encoding='utf-8')
            f.write(news)
            f.close()
        except:
            continue
        
def get_news(headers, url):
    print('get_news函数'+url)
    #--------------获取有多少页------------------#
    url_get = requests.get(url + '/index.html')
    soup = BeautifulSoup(url_get.content.decode(), 'lxml')
    class_common_inactive = soup.find('span', class_ = 'common inactive').get_text()
    page_count = re.sub("\D", "", class_common_inactive)
    #-------------------------------------------#
    page_count = int(page_count)
    get_content(url, 0)
    for i in range(1,page_count):
        get_content(url, i)


headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
url_pool = ['http://www.cnic.cas.cn/xwdt/zhxw',
           'http://www.cnic.cas.cn/xwdt/yfdt',
           'http://www.cnic.cas.cn/xwdt/ttxw',
           'http://www.cnic.cas.cn/tzgg/tz',
           'http://www.cnic.cas.cn/hzjl/gjhz/hzdt',
           'http://www.cnic.cas.cn/yjsjy/tzgg',
           'http://www.cnic.cas.cn/yjsjy/zsjy']
for n in range(9):
    get_news(headers,url_pool[n])