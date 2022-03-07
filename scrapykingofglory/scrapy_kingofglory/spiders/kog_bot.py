import scrapy
from lxml import etree
from scrapykingofglory.scrapy_kingofglory.items import ScrapyKingofgloryItem

class KogBotSpider(scrapy.Spider):
    name = 'kog_bot'
    # allowed_domains = ['pvp.qqq.com']
    def start_requests(self):
        url = 'https://pvp.qq.com/web201605/herolist.shtml'
        yield scrapy.Request(url=url)

    def parse(self, response):
        # 创建kog_etree
        kog_etree = etree.HTML(response.text)
        # 进行查找对应的url
        all_urls = kog_etree.xpath('//div[@class="herolist-content"]/ul/li/a/@href')
        # 获取所有英雄的信息
        for url in all_urls:
            # 对获取到的数据进行处理得到英雄id
            hero_id = url.split('/')[1].split('.')[0]
            # 对获取到的数据进行处理得到英雄url
            hero_url = 'https://pvp.qq.com/web201605/'+url
            # 产生一个request
            yield scrapy.Request(url=hero_url, callback=self.parse_hero, meta={'hero_id': hero_id})

    def parse_hero(self, response):
        # 英雄id
        hero_id = response.meta['hero_id']
        # 创建hero_skin_etree
        hero_skin_etree = etree.HTML(response.text)
        # 英雄的所有皮肤
        hero_skin_names = hero_skin_etree.xpath('//div[@class="pic-pf"]/ul/@data-imgname')[0]
        # 获取图片的url
        for count in range(1, len(hero_skin_names.split('|'))+1):
            # 进行实例化
            item = ScrapyKingofgloryItem()
            # 拼接url
            goal_url = 'https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/'+hero_id+'/'+hero_id+'-mobileskin-'+str(count)+'.jpg'
            final_url = [goal_url]
            # 产生item
            item['image_urls'] = final_url
            yield item
