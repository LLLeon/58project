import time
from page_parsing import url_list, item_info  # 调用数据库中的表

while True:
    # print('url_list:', url_list.find().count())  # 对数据库中条目进行计数, 以观察抓取了多少条信息
    # time.sleep(5)
    print('item_info:', item_info.find().count())
    time.sleep(5)