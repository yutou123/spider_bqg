#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,re,json,requests as req

reload(sys)
sys.setdefaultencoding('utf-8')

from ua import *
from lxml import etree

import cStringIO


class SpiderBiquge_content(object):
    """docstring for ClassName"""
    def __init__(self, url):
        # super(SpiderBiquge, self).__init__()
        # self.arg = arg
        self.f_content = cStringIO.StringIO()


        self.zj  = []
        self.host = "http://www.biqudu.com"
        self.url = url

        self.book_name = ''
        self.author = ''
        self.category = ''
        self.description = ''
        self.image = ''
        self.charset = ''

        self.title = ''
        self.content = ''

    def __delete__(self):

        self.f_content.close()


    # # 获取内容
    def get_html(self,url):
        try:
            resp= req.get(url,headers = {'User-Agent':model_headers()})
            self.charset = resp.encoding
            resp.encoding = 'utf-8'
            re_conten = resp.content
            if(resp.status_code != 200 ):
                re_conten = False
        except Exception as e:
            re_conten = False
            print("erro:",e)
        finally:
            return re_conten

    #写入内存
    def  w_stingio(self,content):
            self.f_content.seek(0)
            self.f_content.write(content)
            self.f_content.flush()

    def read_stingio(self):
            self.f_content.seek(0)
            return self.f_content.read()

    #XML 转 字符串
    def tostring(self,xo):
        return etree.tostring(xo,pretty_print=True,encoding='utf-8')




    def main(self):
        # print self.url
        re_conten = self.get_html(self.url)
        if re_conten :
            html =  etree.HTML(re_conten)
            wz_title  = html.xpath('//h1/text()')

            self.title = wz_title[0].strip()

        # //判断正文位置
            result =  html.xpath('//*[@id=\"content\"]')
            list_con =  self.tostring(result[0])
            re_con = re.findall(r'(?<=<script>{0}\</script\>)([\S\s]*?)(?={1})'.format('readx\(\);','\<script\>'),list_con)
            self.content = re_con[0].strip()
        #     # print "diyiy"
            json_dict = {
                'url':self.url,
                'title':self.title,
                'content':self.content

            }

            return  json.dumps(json_dict)
if __name__ == '__main__':
    # url = "http://www.biqudu.com/22_22901/" #章节URL
    url =  "http://www.biqudu.com/22_22901/1381251.html"
    print SpiderBiquge_content(url).main()
   