import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import requests
import time
import queue
import threading
from lxml.html import fromstring
import tqdm
import pickle as pkl


global stage_set
stage_set = set()
global news
news = []
global news_counter
news_counter = 1
it_url_list = []
url_queue = queue.Queue()
url_limit = 2001
baseurl = 'https://www.toutiao.com/ch/news_hot/'
url = 'https://www.toutiao.com'
global news_pkl_counter
news_pkl_counter = 0
global url_pkl_counter
url_pkl_counter = 0
global same_check
same_check=0

def get_url(baseurl):
    global url_pkl_counter
    global stage_set
    global same_check
    base_url = baseurl
    firefox_options = Options()
    #firefox_options.set_headless()
    driver = webdriver.Firefox(firefox_options=firefox_options)
    driver.get(base_url)
    driver.implicitly_wait(10)
    incre_count = 0
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0,0)")
    time.sleep(3)
    while len(stage_set) < url_limit:
        for i in range(10):
            js = "window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;"
            driver.execute_script(js)
            time.sleep(2)
        time.sleep(2) 
        html = driver.page_source
        tree = fromstring(html)
        try:
            temp_list = tree.xpath('//a[@class="link title"]/@href')
        except:
            temp_list = tree.xpath('//a[@class="link"]/@href')
        
        temp_set = set(temp_list)
        increment = temp_set.difference(stage_set)
        stage_set = stage_set.union(temp_set)
        
        for item in increment:
            full_url = url + item
            it_url_list.append(full_url)
            url_queue.put(full_url)
            url_queue.task_done()
            incre_count = incre_count + 1
             
             
        if(incre_count > 1998):
            with open(r'/root/Desktop/fxl/org_data/today_url_'+str(eval('url_pkl_counter'))+'.pkl','wb') as f: 
                pkl.dump(it_url_list,f,pkl.HIGHEST_PROTOCOL)
            url_pkl_counter = url_pkl_counter + 1
            incre_count = 0
            it_url_list.clear()

        if(same_check == len(it_url_list)):
            break
        else:
            same_check = len(it_url_list)
        print(len(it_url_list))
    with open(r'/root/Desktop/fxl/org_data/today_url_'+str(eval('url_pkl_counter'))+'.pkl','wb') as f:
        pkl.dump(it_url_list,f,pkl.HIGHEST_PROTOCOL)
    driver.close()
    

def get_content():
    global news_pkl_counter
    global news
    global news_counter
    while not url_queue.empty():
        news_url = url_queue.get()
        news_url = re.sub(r'group/','a',news_url)
        news_page = requests.get(news_url)
        news_html = news_page.text
        title0 = re.findall(r'title:(.+),',news_html)
        try:
            title = title0[0]
        except:
            title = ''
        content0 = re.findall(r'content:(.+),',news_html)
        try:
            content = content0[0]
        except:
            content = ''
        news_temp = [title,content]
        news.append(news_temp)
        if(news_counter == 1000):
            with open(r'/root/Desktop/fxl/org_data/today_news_'+str(eval('news_pkl_counter'))+'.pkl','wb') as f:
                pkl.dump(news,f,pkl.HIGHEST_PROTOCOL)
            news_pkl_counter = news_pkl_counter + 1
            news_counter = 0
            news = []
        news_counter = news_counter + 1  
    with open(r'/root/Desktop/fxl/org_data/today_news_'+str(eval('news_pkl_counter'))+'.pkl','wb') as f:
        pkl.dump(news,f,pkl.HIGHEST_PROTOCOL)
    news_counter = 1
    news_pkl_counter = news_pkl_counter + 1
    

threading.Thread(target = get_url,args=('https://www.toutiao.com/ch/news_hot/',)).start()
time.sleep(60)
while True:
    #threading.Thread(target = get_content,args=()).start()
    get_content()
    time.sleep(75)
    if(url_queue.empty()):
        break
