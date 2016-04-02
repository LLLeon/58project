from bs4 import BeautifulSoup
import requests
import time
import pymongo


start_url = 'http://bj.58.com/shoujihao/pn1'
client = pymongo.MongoClient('localhost', 27017)
phone_number = client['phone_number']
number_info = phone_number['number_info']


# spider 1 获取手机号码标题及网址
def get_number_info(pages):
    start_url = ['http://bj.58.com/shoujihao/pn{}'.format(str(i)) for i in range(1, pages+1)]
    for url in start_url:
        wb_data = requests.get(url)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        if soup.find('strong', 'number'):  # 判断页面中是否有商品
            links = soup.select('div > ul > div > ul > li > a.t')
            titles = soup.select('li > a.t > strong')
            prices = soup.select('b.price')
            for link, title, price in zip(links, titles, prices):
                data  = {
                    'link': link.get('href'),
                    'title': title.get_text(),
                    'price': int(price.get_text().strip('元'))
                }
                if data['link'].split('.')[0] != 'http://bj':  # 判断是否是正式商品
                    pass
                else:
                    number_info.insert_one(data)
                    print(data)
        else:
            pass


get_number_info(116)
