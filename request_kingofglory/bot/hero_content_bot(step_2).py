# -*- encoding : utf-8 -*-
# @Author : Fenglchen
import requests
from lxml import etree
import os
from request_kingofglory.bot.content_bot import download_hero_skin
from request_kingofglory.bot.content_bot import download_hero_message


# 请求头
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
    'referer': 'https://pvp.qq.com/raiders/',
}

# 获得当前脚本存放的父目录的绝对路径
project_path = os.path.abspath('..')
# 进行路径拼接 拼接完整的all_urls.txt路径
project_path = os.path.join(project_path, 'pool', 'all_urls.txt')
# 读取step_1中所获取到的url
with open(project_path, mode='r') as read_au:
    # 将文件读取到的内容存储到temp_all_urls
    temp_all_urls = read_au.read()
# 进行数据处理 获取到all_urls
all_urls = temp_all_urls.split('\n')[:-1]

# 获得当前脚本存放的父目录的绝对路径
project_path = os.path.abspath('..')
# 进行路径拼接 拼接完整的英雄文件夹路径
project_path = os.path.join(project_path, 'pool', 'success_urls.txt')
# 读取已经写入过的英雄链接
with open(project_path, mode='r') as read_suc:
    # 将文件读取到的内容存储到temp_success_urls
    temp_success_urls = read_suc.read()
# 成功获取全部信息的url
success_urls = {}
# 当前存在下载成功的url
if len(temp_success_urls) != 0:
    # 进行数据处理 获取到success_urls
    for url in temp_success_urls.split('\n')[:-1]:
        success_urls[url.split('\t')[0]] = url.split('\t')[1]


# 进行遍历获取对应的信息
for goal_url in all_urls:
    # 检测是否被下载过
    if goal_url in success_urls:
        print('检测到当前英雄：{}已下载！已跳过！'.format(success_urls[goal_url]))
        continue
    # 获得的响应
    response = requests.get(url=goal_url, headers=headers)
    # 网站charset为gbk 所以需要转换为二进制再重新解码
    response = response.content.decode('GBK')
    # 创建hero_etree
    hero_etree = etree.HTML(response)

    # 当前url所对应的英雄信息
    hero_name = hero_etree.xpath('//div[@class="cover"]/h2/text()')[0]

    # 技能名字
    skill_name = hero_etree.xpath('//div[@class="skill-show"]/div/p[1]/b/text()')
    # 技能冷却
    skill_cd = hero_etree.xpath('//div[@class="skill-show"]/div/p[1]/span[1]/text()')
    # 技能消耗
    skill_consume = hero_etree.xpath('//div[@class="skill-show"]/div/p[1]/span[2]/text()')
    # 技能介绍
    skill_desc = hero_etree.xpath('//div[@class="skill-show"]/div/p[2]/text()')
    # 英雄技能
    hero_skill = zip(skill_name, skill_cd, skill_consume, skill_desc)

    # 英雄技巧
    hero_tips = hero_etree.xpath('//div[@class="equip-bd"]/div/p/text()')

    # 英雄故事
    hero_story = hero_etree.xpath('//div[@class="pop-story"]/div[2]/p/text()')[0]

    # 英雄的所有皮肤
    hero_skin_url = hero_etree.xpath('//div[@class="cover"]/a/img/@src')[0]
    # 英雄的所有皮肤名字存入temp_hero_skin_name
    temp_hero_skin_names = hero_etree.xpath('//div[@class="pic-pf"]/ul/@data-imgname')[0]
    # 英雄所有皮肤的名字
    hero_skin_names = []
    # 将获取到的数据进行处理
    for skin_name in temp_hero_skin_names.split('|'):
        hero_skin_names.append(skin_name.split('&')[0])

    # 返回提示
    print('开始下载英雄:{}的皮肤......'.format(hero_name))
    # 进行下载该英雄的皮肤
    download_hero_skin(hero_name, hero_skin_url, hero_skin_names)
    print('下载完成！共:{}款！'.format(len(hero_skin_names)))

    # 返回提示
    print('开始下载英雄的相关信息:{}......'.format(hero_name))
    # 进行下载该英雄的相关信息
    download_hero_message(hero_name=hero_name, hero_skill=hero_skill, hero_tips=hero_tips,
                          hero_story=hero_story, hero_url=goal_url)
    print('下载完成!')

# 全部下载完成后返回提示
print('****************************')
print('全部下载完成！总共：{}位英雄！'.format(len(all_urls)))
print('****************************')

