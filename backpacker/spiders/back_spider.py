# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
from backpacker.items import BackpackerItem
import time
class BackSpiderSpider(scrapy.Spider):
    name = 'back-spider'
    allowed_domains = ['backpackers.com.tw']
    start_urls = ['https://www.backpackers.com.tw/forum/forumdisplay.php?f=25']
    
    def parse(self, response):

        #old version
        ####################################################################################################################
        # form  = response.xpath('//tbody[starts-with(@id,"threadbits")]') 
        # trs = form.xpath('.//tr')   
        # for tr in trs:
        #     if tr.xpath('.//td[@colspan]//ins[@class]').extract_first() is not None:
        #         pass
        #     else:
        #         title = tr.xpath('.//td[starts-with(@id,"td_threadtitle_")]//a[starts-with(@href,"showthread")]//text()').extract_first()
        #         last_reply = tr.xpath('.//td[starts-with(@title,"回覆")]/div[@class="smallfont"]/text()').extract_first().lstrip()
        #         num_of_reply = tr.xpath('.//td[@class = "alt1 smallfont"]/text()').extract_first()
        #         num_of_view = tr.xpath('.//td[@class = "alt2 smallfont"]/text()').extract_first()
                
        #         thread = {'title':title,
        #                   'last_reply':last_reply,
        #                   'num_of_reply':num_of_reply,
        #                   'num_of_view':num_of_view}
        #         yield thread

        #     if response.xpath('//td//a[@rel="next"]/@href').extract_first() is not "":
        #         next_btn_url = response.xpath('//td//a[@rel="next"]/@href').extract_first()
        #         absolute_next_btn_url = response.urljoin(next_btn_url)
        #         yield scrapy.Request(url=absolute_next_btn_url,callback=self.parse)
        ####################################################################################################################


        #new version

        forum =response.xpath('//tbody[@id="threadbits_forum_25"]')
        trs = forum.xpath('./tr')
        for tr in trs:
            #exclude google ad post
            if tr.xpath('./td[@colspan]').extract_first() is None:
                url = tr.xpath('./td/div/a/@href').extract_first()
                abs_url = response.urljoin(url)
                #post_last_reply = response.xpath('.//div[@class = "smallfont" and @style = "text-align:right; white-space:nowrap"]/text()').extract()
                #post_last_reply = list(map(lambda s: s.strip(),post_last_reply))
                #yield{'post_last_reply':post_last_reply}

            #forwarded to every single post in a page
            yield Request(url = abs_url, callback= self.parse_thread_content)
        
        #click to next page
        next_btn_url = response.xpath('//a[@rel="next"]/@href').extract_first()
        absolute_next_btn_url = response.urljoin(next_btn_url)
        
        #recursive function used to loop through all pages and send requests for each post
        yield Request(url = absolute_next_btn_url, callback= self.parse)


    #post content crawling
    def parse_thread_content (self, response):

        # # scrap post title only when it is in page 1 of the post
        if response.xpath('//a[@rel="prev"]//text()').extract_first() is None:
            post_title = response.xpath('//h1//text()').extract_first().strip()
            yield{'post_title': post_title}

        #all the reply in the current page of current post
        replies = response.xpath('//div[starts-with(@id,"post_message")]')

        #content of every reply
        for reply in replies:
            content = reply.xpath('.//text()').extract()
            #strip '/n' and '/t' off from text in a list
            content = list(map(lambda s: s.strip(),content))
            reply_created_on = response.xpath('.//td[starts-with(@id,"td_post_")]//div[@class = "smallfont"]/text()').extract()[5].strip()   
            yield{'reply_created_on':reply_created_on,
                  'content':content}


        #click next page
        if response.xpath('//a[@rel="next"]/@href').extract_first() is not None:
            next_btn_in_content_page = response.xpath('//a[@rel="next"]/@href').extract_first()
            abs_next_btn_url_in_content_page = response.urljoin(next_btn_in_content_page)

            yield Request(url = abs_next_btn_url_in_content_page, callback= self.parse_thread_content)
        # else:
        #     post_title = response.xpath('//h1//text()').extract_first().strip()
        #     yield{
        #         'post_title':post_title
        #         'content':post_list
        #     }






            

      


    	

    


    		
    		




        
