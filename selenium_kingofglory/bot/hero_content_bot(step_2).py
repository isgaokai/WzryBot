# -*- encoding : utf-8 -*-
# @Author : Fenglchen
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
import os


# 请求头
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
    'referer': 'https://pvp.qq.com/raiders/',
}


# 创建一个谷歌窗口
browser = webdriver.Chrome()
# 获得当前脚本存放的父目录的绝对路径
project_path = os.path.abspath('..')
# 进行路径拼接 拼接完整的英雄文件夹路径
project_path = os.path.join(project_path, 'pool', 'all_hero_urls.txt')
# 读取step_1中所获取到的url
with open(project_path,mode='r') as read_a_h_u:
    temp_all_urls = read_a_h_u.read()
all_urls = {}
# 对获取到的数据进行处理
for url in temp_all_urls.split('\n')[:-1]:
    all_urls[url.split('\t')[0]] = url.split('\t')[1]

# 获得当前脚本存放的父目录的绝对路径
project_path = os.path.abspath('..')
# 进行路径拼接 拼接完整的英雄文件夹路径
project_path = os.path.join(project_path, 'pool', 'success_urls.txt')
# 读取已经写入过的英雄链接
with open(project_path, mode='r') as read_suc:
    # 将文件读取到的内容存储到temp_success_urls
    temp_success_urls = read_suc.read()
# 成功获取全部信息的url
success_urls = []
# 当前存在下载成功的url
if len(temp_success_urls) != 0:
    # 进行数据处理 获取到success_urls
    for url in temp_success_urls.split('\n')[:-1]:
        success_urls.append(url)

# 进行遍历获取对应的信息
for hero_url, hero_name in all_urls.items():
    # 检测是否被下载过
    if hero_url in success_urls:
        print('检测到当前英雄：{}已下载！已跳过！'.format(hero_name))
        continue
    # 发送请求
    browser.get(url=hero_url)
    # 显性等待
    locator = (By.XPATH, '//div[@class="pic-pf"]/ul/li')
    WebDriverWait(browser, 2, 0.5).until(EC.element_to_be_clickable(locator))
    # 当前英雄的皮肤信息
    hero_skin = browser.find_elements_by_xpath('//div[@class="pic-pf"]/ul/li/i/img')

    # 获得当前脚本存放的父目录的绝对路径
    project_path = os.path.abspath('..')
    # 进行路径拼接 拼接完整的英雄文件夹路径
    project_path = os.path.join(project_path, 'hero', hero_name)
    # 进行创建对应英雄的文件夹
    try:
        os.mkdir(project_path)
    # 文件夹已经创建
    except:
        pass

    # 返回提示
    print('开始下载英雄:{}的皮肤......'.format(hero_name))
    # 下载英雄的皮肤并进行保存
    for skin in hero_skin:
        # 目标url
        goal_url = 'https:'+skin.get_attribute('data-imgname')
        # 对应皮肤名称
        skin_name = skin.get_attribute('data-title')
        # 获得对应的响应
        response = requests.get(url=goal_url)
        # 获得当前脚本存放的父目录的绝对路径
        project_path = os.path.abspath('..')
        # 进行路径拼接 拼接完整的英雄文件夹路径
        project_path = os.path.join(project_path, 'hero', hero_name, skin_name+'.jpg')
        # 进行写入保存皮肤
        with open(project_path, mode='wb') as download_skin:
            download_skin.write(response.content)

    # 获得当前脚本存放的父目录的绝对路径
    project_path = os.path.abspath('..')
    # 进行路径拼接 拼接完整的英雄文件夹路径
    project_path = os.path.join(project_path, 'pool', 'success_urls.txt')
    # 将获取完全英雄的链接进行写入保存
    with open(project_path, mode='a+') as write_suc:
        write_suc.write(hero_url)
        write_suc.write('\n')

    print('下载完成！共:{}款！'.format(len(hero_skin)))

# 全部下载完成后返回提示
print('****************************')
print('全部下载完成！总共：{}位英雄！'.format(len(all_urls)))
print('****************************')
browser.close()
