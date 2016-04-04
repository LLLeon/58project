from bs4 import BeautifulSoup
import requests
import time
import pymongo


client = pymongo.MongoClient('localhost', 27017)
page_parsing = client['page_parsing']
url_list = page_parsing['url_list']
item_info = page_parsing['item_info']


# spider 1 抓取商品链接
def get_links_from(channel, pages, who_sells=0):  # channel: 频道链接, pages: 第几页, who: 个人or商家
    #http://bj.58.com/shouji/0/pn2/
    list_view = '{}{}/pn{}/'.format(channel, str(who_sells), str(pages))  # 拼接列表页网址
    wb_data = requests.get(list_view)
    time.sleep(1)
    soup = BeautifulSoup(wb_data.text, 'lxml')

    # 判断页面中是否有td标签class为t元素,如有才有商品
    if soup.find('td', 't'):
        for link in soup.select('td.t a.t'):
            item_link = link.get('href').split('?')[0]
            if 'zhuanzhuan' in item_link:
                pass

            # 检测数据库中是否已有此数据, 如无则继续存入
            elif url_list.find_one({'url': item_link}) is None:
                url_list.insert_one({'url': item_link})
                print('已插入:', item_link)
            else:
                print('已有此条数据...')
    else:
        pass

# get_links_from('http://bj.58.com/shuma/', 2)

# spider 2 抓取商品详情
def get_item_info(url):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, 'lxml')

    # 判断该页面是否有商品, 如无商品则pass
    no_longer_exit = '404' in soup.find('script', type='text/javascript').get('src').split('/')
    if no_longer_exit in soup:
        pass
    else:
        title = soup.title.text
        price = list(soup.select('span.price.c_f50')[0].stripped_strings)[0].replace(' 元', '')  # 观察不用类型价钱位置可能有空格,进行stripped_strings处理
        date = soup.select('.time')[0].text
        area = list(soup.select('div.col_sub.sumary > ul > li:nth-of-type(3) > div.su_con > span.c_25d')[0].stripped_strings) if soup.find_all('span', 'c_25d') else None

        # 检查是否已存入数据库, 如未存入则继续存入
        if item_info.find_one({'title': title}) is None:
            item_info.insert_one({'title': title, 'price': price, 'date': date, 'area': area})
            print('已插入:', {'title': title, 'price': price, 'date': date, 'area': area})
        else:
            print('已有此条数据...')


# 测试
# for url in url_list.find():
#     get_item_info(url['url'])

#print([urls['url'] for urls in url_list.find()])

#print(map(get_item_info, [urls['url'] for urls in url_list.find()]))