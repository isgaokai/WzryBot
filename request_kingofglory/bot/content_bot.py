# -*- encoding : utf-8 -*-
# @Author : Fenglchen
import requests
import os

# 请求头
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
    'referer': 'https://pvp.qq.com/raiders/',
}


# 下载英雄的皮肤
def download_hero_skin(hero_name=None, start_url=None, skin_names=None):
    '''
    :param hero_name: 对应英雄的名字
    :param start_url: 对应英雄皮肤起始的url
    :param skin_names: 所有皮肤的名字
    :return:
    '''
    # 讲传入的start_url 进行处理
    start_url = 'https:'+start_url[:65]
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
    # 进行遍历进行下载
    for index, value in enumerate(skin_names):
        # 进行拼接得到目标皮肤的url
        goal_url = start_url + str(index+1) + '.jpg'
        # 获得对应的响应
        response = requests.get(url=goal_url, headers=headers)
        # 获得当前脚本存放的父目录的绝对路径
        project_path = os.path.abspath('..')
        # 进行路径拼接 拼接完整的英雄文件夹路径
        project_path = os.path.join(project_path, 'hero', hero_name)
        # 对应皮肤的文件路径
        value = value+'.jpg'
        project_path = os.path.join(project_path, value)
        # 进行写入保存皮肤
        with open(project_path, mode='wb') as download_skin:
            download_skin.write(response.content)


# 下载英雄的相关信息
def download_hero_message(hero_name=None, hero_skill=None, hero_tips=None, hero_story=None, hero_url=None):
    '''

    :param hero_name: 对应英雄的名字
    :param hero_skill: 对应英雄的技能
    :param hero_tips: 对应英雄的提示
    :param hero_story: 对应英雄的故事
    :param hero_url: 对应英雄的url
    :return:
    '''
    # 获得当前脚本存放的父目录的绝对路径
    project_path = os.path.abspath('..')
    # 进行路径拼接 拼接完整的英雄文件夹路径
    project_path = os.path.join(project_path, 'hero', hero_name, hero_name+'.txt')
    # 进行写入相关信息
    with open(project_path, mode='w') as download_mess:
        # 写入英雄名
        download_mess.write('英雄名：'+hero_name)
        download_mess.write('\n\n')
        # 写入英雄技能
        download_mess.write('英雄技能：'+'\n')
        for skill in hero_skill:
            for content in skill:
                download_mess.write(content)
                download_mess.write(' ')
            download_mess.write('\n\n')
        # 写入英雄技巧
        download_mess.write('英雄技巧：'+'\n')
        for tip in hero_tips:
            download_mess.write(tip)
            download_mess.write('\n\n')
        # 写入英雄故事
        download_mess.write('英雄故事：'+'\n')
        download_mess.write(hero_story)
        download_mess.write('\n\n')
        # 写入英雄链接
        download_mess.write('英雄链接：')
        download_mess.write(hero_url)

    # 获得当前脚本存放的父目录的绝对路径
    project_path = os.path.abspath('..')
    # 进行路径拼接 拼接完整的英雄文件夹路径
    project_path = os.path.join(project_path, 'pool', 'success_urls.txt')
    # 将获取完全英雄的链接进行写入保存
    with open(project_path, mode='a+') as write_suc:
        write_suc.write(hero_url)
        write_suc.write('\t')
        write_suc.write(hero_name)
        write_suc.write('\n')

