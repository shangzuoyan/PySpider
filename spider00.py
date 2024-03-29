#-*- coding: UTF-8 -*-

from concurrent.futures import ThreadPoolExecutor
from imp import reload
import io
import sys
import time
import requests
import numpy as np
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


#Some User Agents
hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
{'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
{'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]

#笔趣阁网站
siteUrl='https://www.bqgka.com'
#小说《秦功》主页
bookUrl='https://www.bqgka.com/book/112833/'



#下载全书章节到本地
def dl_chapters(url):
    #url='https://www.bqgka.com/book/112833/' # For Test
    plain_text = requests.get(url, headers=hds[np.random.randint(0,len(hds))]).text
    soup = BeautifulSoup(plain_text)
    chapter_obj = soup.find('h1',{'class':'wap_none'})
    content_obj = soup.find('div',{'id':'chaptercontent'})
    if chapter_obj and content_obj:
        ch = chapter_obj.get_text()
        ct = content_obj.get_text()
        #print ch
        with open(f"book/{ch}.txt","w") as f:
            f.write(ct)
        print(f"{ch} Downloaded")


#获取全书章节列表并下载至本地文本文件
def get_book(url):
    #url='https://www.bqgka.com/book/112833/' # For Test
    plain_text = requests.get(url, headers=hds[np.random.randint(0,len(hds))]).text
    soup = BeautifulSoup(plain_text)
    items=soup.find('div',{'class':'listmain'}).findAll('a')
    chUrls=[] ##全书所有章节URL
    for item in items:
        ##<a href="javascript:dd_show()" rel="nofollow">&lt;&lt;---展开全部章节---&gt;&gt;</a>
        href = item["href"]
        if href!="javascript:dd_show()":
            print(siteUrl+href)
            chUrls.append(siteUrl+href)

    ##单线程下载
    #dl_chapters(chUrls)
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