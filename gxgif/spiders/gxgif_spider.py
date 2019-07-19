# -*- coding: utf-8 -*-
import scrapy

from gxgif.items import GxgifItem


class GxgifSpiderSpider(scrapy.Spider):
    name = 'gxgif_spider'

    allowed_domains = ['www.gaoxiaogif.com']
    start_urls = ['http://www.gaoxiaogif.com']

    def parse(self, response):
        gif_list = response.xpath("//div[@class='listgif-box']")
        for i_item in gif_list:
            gif_item = GxgifItem()
            gif_item['title'] = i_item.xpath(".//a/text()").extract_first()
            gif_item['content'] = eval(i_item.xpath(".//div[@id='bdshare']//@data").extract_first())['pic']
            gif_item['tag'] = i_item.xpath(".//div[@class='tagsinfo']//a/text()").extract_first()
            gif_item['content_type'] = 'image'
            if  len(str(gif_item['title']))== 0:
                gif_item['title'] = " "
            if len(str(gif_item['tag'])) == 0:
                gif_item['tag'] = " "


    #        print(gif_item)
        yield gif_item

        next_link = response.xpath("//a[text()='下一页']/@href").extract()
       # if next_link and not (next_link=='/index_5.html'):
        if not (next_link[0] == '/index_309.html'):
            next_link = next_link[0]
            print(next_link)
            yield scrapy.Request(self.start_urls[0] + next_link, callback=self.parse)


