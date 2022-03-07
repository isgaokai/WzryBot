# -*- encoding : utf-8 -*-
# @Author : Fenglchen
import requests
from lxml import etree
import os


# 请求头
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
    'referer': 'https://pvp.qq.com/raiders/',
}

# 目标url
goal_url = 'https://pvp.qq.com/web201605/herolist.shtml'
# 获得的响应
response = requests.get(url=goal_url, headers=headers)

# 判断响应状态码是否为200
if response.status_code == 200:
    # 创建kog_etree
    kog_etree = etree.HTML(response.text)
    # 进行查找对应的url
    all_urls = kog_etree.xpath('//div[@class="herolist-content"]/ul/li/a/@href')
    # 获得当前脚本存放的父目录的绝对路径
    project_path = os.path.abspath('..')
    # 进行路径拼接 拼接完整的all_urls.txt路径
    project_path = os.path.join(project_path, 'pool', 'all_urls.txt')
    # 进行写入获取到的url
    with open(project_path, mode='w') as write_au:
        # 遍历写入
        for url in all_urls:
            # xpath获取到的非完整链接 所以进行字符串拼接
            write_au.write('https://pvp.qq.com/web201605/'+url)
            # 换行操作
            write_au.write('\n')
    # 写入成功 返回提示
    print('写入成功！总共获取到{}位英雄的链接！'.format(len(all_urls)))

# 无法正常访问网页时，返回对应显示的状态码
else:
    print('无法正确访问网页，网页响应码为:{}!'.format(response.status_code))
