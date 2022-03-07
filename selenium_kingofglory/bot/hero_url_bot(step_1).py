# -*- encoding : utf-8 -*-
# @Author : Fenglchen
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os

# 创建一个谷歌窗口
browser = webdriver.Chrome()
# 目标网站的url
goal_url = 'https://pvp.qq.com/web201605/herolist.shtml'
# 发送请求
browser.get(url=goal_url)

# 显性等待
locator = (By.XPATH, '//div[@class="herolist-content"]/ul/li/a')
WebDriverWait(browser, 2, 0.5).until(EC.element_to_be_clickable(locator))

# 获取到所有英雄的信息
temp_all_hero = browser.find_elements_by_xpath('//div[@class="herolist-content"]/ul/li/a')
all_hero = {}
# 对获取到的数据进行处理
for hero in temp_all_hero:
    all_hero[hero.text] = hero.get_attribute('href')

# 获得当前脚本存放的父目录的绝对路径
project_path = os.path.abspath('..')
# 进行路径拼接 拼接完整的英雄文件夹路径
project_path = os.path.join(project_path, 'pool', 'all_hero_urls.txt')
# 将获取到到数据进行写入保存
with open(project_path, mode='w') as write_a_h_u:
    for key, value in all_hero.items():
        write_a_h_u.write(value)
        write_a_h_u.write('\t')
        write_a_h_u.write(key)
        write_a_h_u.write('\n')
# 进行关闭
browser.close()
