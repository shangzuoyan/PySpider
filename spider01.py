#-*- coding: UTF-8 -*-

from concurrent.futures import ThreadPoolExecutor

import time
import requests
import numpy as np
from bs4 import BeautifulSoup

#reload(sys)
#sys.setdefaultencoding('utf8')
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


#Some User Agents
hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
{'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
{'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]

#URL
protocolUrl='https:'
#侠客中文网
siteUrl='https://www.xiakabbb.com/'
#小说《寒门差役》目录页
bookUrl='https://www.xiakabbb.com/txt65866.shtml'



#下载全书章节到本地
def dl_chapters(url):
    plain_text = requests.get(url, headers=hds[np.random.randint(0,len(hds))]).text
    soup = BeautifulSoup(plain_text)
    chapter_obj = soup.find('div',{'class':'bookname'}).find('h1')
    content_obj = soup.find('div',{'id':'content'})
    if chapter_obj and content_obj:
        ch = chapter_obj.get_text()
        ct = content_obj.get_text()
        #print ch
        with open(f"book01/{ch}.txt","w") as f:
            f.write(ct)
        print(f"{ch} Downloaded")


#获取全书章节列表并下载至本地文本文件
def get_book(url):
    plain_text = requests.get(url, headers=hds[np.random.randint(0,len(hds))]).text
    soup = BeautifulSoup(plain_text)
    items=soup.find('div',{'id':'list'}).findAll('a')
    chUrls=[] ##全书所有章节URL
    for item in items:
        href = item["href"]
        ##if href!="javascript:dd_show()":
        ##print(protocolUrl+href)
        chUrls.append(protocolUrl+href)
        ##单线程下载
        #dl_chapters(protocolUrl+href)


    ##多线程下载
    with ThreadPoolExecutor(max_workers=len(chUrls)) as exe:
        for urlx in chUrls:
            exe.submit(dl_chapters,urlx)

############################################################



if __name__=='__main__':
    btm = time.time()
    get_book(bookUrl)
    etm = time.time()
    print(f"Total Time:{(etm-btm)}s")