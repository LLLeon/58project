from multiprocessing import Pool  # 导入多进程库
from channel_extract import channel_list
from page_parsing import get_links_from, get_item_info, url_list


def get_all_links_from(channel):  # 抓取所有类型商品及页面详情
    for num in range(1, 101):
        get_links_from(channel, num)


# def get_all_info_from(url):
#     for urls in url_list.find():
#         get_item_info(urls['url'])

if __name__ == '__main__':
    pool = Pool()  # 定义进程池
    pool.map(get_all_links_from, channel_list.split())  # 调用进程池
    pool.map(get_item_info, [urls['url'] for urls in url_list.find()])