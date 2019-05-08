#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,re,json,requests as req

reload(sys)
sys.setdefaultencoding('utf-8')

from ua import *
from lxml import etree

import cStringIO

class SpiderBiquge(object):
    """docstring for ClassName"""
    def __init__(self, url):
        # super(SpiderBiquge, self).__init__()
        # self.arg = arg
        self.f_content = cStringIO.StringIO()
        self.zhangjie = {}
      
        self.zj  = []
        self.host = "http://www.biqudu.com"
        self.url = url
        self.status = ''
    
        self.book_name = ''
        self.author = ''
        self.category = ''
        self.description = ''
        self.image = ''
        self.charset = ''


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

    # #输出最后内容
    def a_con(self,zj_num,content):
        zj_html =  etree.HTML(content)
        result_dd = zj_html.xpath(u'//a')

        for i,href in enumerate(result_dd):
            self.zhangjie.setdefault(zj_num,{})[i]= {
                'url':self.host + href.attrib['href'],
                'title':href.text.encode(self.charset).replace(':',' '),
                'volumes ':zj_num
            }
        #
        # for i,href in enumerate(result_dd):
        #     url = self.host + href.attrib['href']
        #     title = href.text.encode(self.charset).replace(':',' ')
        #     print re.sub('.*?章','',title)

            # self.zhangjie.setdefault(zj_num,{})[i]= {
            #     'url':,
            #     'title':,

            # }



    def main(self):
        # print self.url
        re_conten = self.get_html(self.url)
        if re_conten :
            html =  etree.HTML(re_conten)
            meta_list  = html.xpath('//head//meta')
           
            for meta_id in meta_list:
                try:
                    meta_propertys  = meta_id.attrib['property']
                    meta_contents = meta_id.attrib['content'].strip()
                except Exception as e:
                    pass
                else:
               
        
                    if 'book_name' in meta_propertys:
                        self.book_name = meta_contents
                        
                    elif 'author' in meta_propertys:
                        self.author = meta_contents

                    elif 'category' in meta_propertys:
                        self.category = meta_contents

                    elif 'status' in meta_propertys:
                        self.status = meta_contents
                    elif 'description' in meta_propertys:
                        # print meta_contents
                        self.description = meta_contents

                    elif 'image' in meta_propertys:
                        # print meta_contents
                        self.image = self.host + meta_contents

            # exit(0)
        # //判断正文位置
            result =  html.xpath('//*[@id=\"list\"]')
            list_con =  self.tostring(result[0])
          
            self.w_stingio(list_con)
            
            result_dt =  html.xpath('//*[@id=\"list\"]//dt')

            for i,x in enumerate(result_dt):
                list_cont = self.read_stingio()

                if u"作品相关" not  in x.text and  i > 0: #排除 第一个dt和相关作品dt
                    dt_title = x.text+'__add__'+ str(i) # 重新设置节点名称
                    print dt_title,x.text
                   #替换标题
                    repa_cont =  re.sub(r'(?<=<dt>).*?{0}(?=</dt>)'.format(x.text),dt_title ,list_cont,1)#循环替换
                    self.w_stingio(repa_cont)
                    dt_title = dt_title.replace(':',' ')
                    self.zj.append(dt_title) #章节名称加入到列表
              
            list_con =   self.read_stingio()
            
            zjnum = len(self.zj)
            print zjnum

            for i,zj_name in enumerate(self.zj):

                if i < zjnum -1:#最后一章节不进行比较
                    print( u"获取章节内容:{0},{1}".format( self.zj[i],self.zj[i+1]))
                    re_con = re.findall(r'(?<=<dt>{0}</dt>)([\S\s]*?)(?={1})'.format(self.zj[i],self.zj[i+1]),list_con)#使用正则匹配 标题1 和标题2 中间内容
                    self.a_con(i,re_con[0])

                else:
                    print( u"获取最后-章节内容:{0}".format(self.zj[i]))
                    re_con = re.findall(r'(?<=<dt>{0}</dt>)([\S\s]*?)(?={1})'.format(self.zj[i],'div'),list_con)
                    self.a_con(i,re_con[0])
                    

                zj_nam = zj_name.split('》')
                zj_name =  zj_nam[1].split('__add__')
                self.zj[i] = zj_name[0]

        #     # print "diyiy"
            json_dict = {
                'url': self.url,
                'status':self.status,
                'book_name':self.book_name,
                'author':self.author,
                'category':self.category,
                'image':self.image,
                'description':self.description,
                'zj_name_list':self.zj,
                'zj_href_list':self.zhangjie}   
                
            return  json.dumps(json_dict)


if __name__ == '__main__':
    url = "http://www.biqudu.com/22_22901/" #章节URL
    print SpiderBiquge(url).main()
   