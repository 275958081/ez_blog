from django.db import models
from DjangoUeditor.models import UEditorField
from DjangoUeditor.commands import *
import redis
import types
import datetime
from redis_accessor import get_redis
# Create your models here.


lp_debug = True 


def debug_print(l):
    print 'the len of l is : ' ,len(l)
    if lp_debug == False :
        return 
    for v in l :
        print v

separator_flag = '__##__'

class ccarticle_tag:
    def __init__(self):
        self.title = ''
        self.url =''

class carticle_type_info:
    def __init__(self):
        self.type_name =''
        self.type_article_number = 0
        self.article_tag_list = []






class carticle_type():
    def __init__(self):
        self.context = ''
        self.blog_number = 0

        '''
        article_type_sed--<type1,type2...>

        type_list--|-type1--[ <title,url> , <title,url> ...]
                          |-type1--[ <title,url> , <title,url> ...]

        article_index_list---------------------<url, title , type ,context,views_times, edit_time,leave_word_times,slug,leave_words_list_key >
         |
         |
         |
        article_leave_words_index--- [ <name , email , time,context> , <name , email , time,context> ]

        @function :  add_article
        @function :  edit_article
        @function :  delete_article
        @function :  read_article

        @function :  add_leave_word
        @function :  read_leave_word

        @function :  add_article_type
        @function :  get_article_type
        @function :  get_article_detail
        '''


 
class cleave_word:
    def __init__(self,article_index,visitor_name,visitor_email,leave_word):
        self.article_index = article_index
        self.visitor_email = visitor_email
        self.visitor_name = visitor_name
        self.leave_word = leave_word
        self.time = str(datetime.datetime.now())[0:19]
        self.index = '-1 '


    @staticmethod
    def create_cleave_word_key(index):
        cleave_word_key = 'article_leave_word_key_' + index
        return cleave_word_key


    def save(self):
        article_cleave_word_key = cleave_word.create_cleave_word_key(self.article_index)
        r = get_redis()
        
        article_leave_word_value = self.self.visitor_email  +separator_flag  + self.index + separator_flag + self.visitor_name +separator_flag + self.time +separator_flag  + self.leave_word
        r.lpush(article_cleave_word_key,article_leave_word_value)
        r.save()

    @staticmethod
    def unserial_leave_word_from_str(s):
        l = s.split(separator_flag)
        if  len(l) <> 4 :
            return None
        article_index = ''
        visitor_email = l[0] ;
        visitor_name = l[1]
        leave_word_time = l[2]
        leave_word = l[3]
        leave_word = cleave_word( article_index ,visitor_name,visitor_email,leave_word)
        return leave_word

    @staticmethod
    def get_blog_leave_words(index):
        blog_leave_word_key = cleave_word.create_cleave_word_key(index)
        r = get_redis()
        leave_words = []
        leave_words_list = r.lrange(blog_leave_word_key , 0 , r.llen(blog_leave_word_key)-1 )
        for leave_word in leave_words_list:
            leave_words.append( cleave_word.unserial_leave_word_from_str( leave_word ) )
        return leave_words
            





class carticle:
    def __init__(self):
        self.title = ''
        self.context = ''
        self.slug =''
        self.time = str( datetime.datetime.now() )[0:19]
        self.url=''
        self.article_h_key = ''
        self.read_times = 0
        self.type = ''
        self.index = -1 ;
        


    def create_article_index(self):
        r = get_redis()
        self.index =  r.incr('__article_index__')
        r.save()


    @staticmethod
    def get_article_h_index(index):
        return ( 'article_ key__' + index)
    
    def create_article_h_key(self):
       self.article_h_key = 'article_ key__' + str(self.index)


    def create_url(self):
         self.url = '/article_' + str(self.index)
 


    @staticmethod
    def create_type_list_key(type):
        type_list_key = 'type_list_'+ type
        return type_list_key

    def create_slug(self):
        self.slug = ''

    @staticmethod
    def get_article_type_key(index):
        article_h_key = carticle.index_to_article_key(index)
        r = get_redis()
        if r.exists( article_h_key ) :
            pass
        else :
            pass


    def save(self):
        self.create_article_index()
        self.create_article_h_key()
        self.create_url()
  
        r = get_redis()
        r.hset(self.article_h_key,'title',self.title)#
        r.hset(self.article_h_key,'context',self.context)#
        r.hset(self.article_h_key,'slug',self.slug)#
        r.hset(self.article_h_key,'time',self.time)#
        r.hset(self.article_h_key,'article_h_key',self.article_h_key)#
        r.hset(self.article_h_key,'url',self.url)#
        r.hset(self.article_h_key,'read_times',self.read_times)
        r.hset(self.article_h_key,'type',self.type)
        r.save()

    @staticmethod
    def get_article(index):
        article = carticle()
        article.index = index 
        article.create_article_h_key()
        r = get_redis()
        if r.exists(article.article_h_key) :
            r.hincrby(article.article_h_key,'read_times')

            article.title = r.hget(article.article_h_key,'title')
            article.context = r.hget(article.article_h_key,'context')
            article.slug = article.slug = r.hget(article.article_h_key,'slug')
            article.time =    r.hget(article.article_h_key,'time')
            article.article_h_key = r.hget(article.article_h_key,'article_h_key')
            article.url =r.hget(article.article_h_key,'url')
            article.read_times =r.hget(article.article_h_key,'read_times')
            article.type =r.hget(article.article_h_key,'type')
            r.save()
            return article
        else :
            return None




    @staticmethod
    def unserial_from_list(sserial_str):
        l = sserial_str.split(separator_flag)
        if len(l) <> 2 :
            print 'unserial_from_list error data, sserial_str : ',sserial_str
            return '',''
        title = l[0]
        url   =l[1]     
        return title,url

  
    def serial_to_list(self): 
       return ( self.title  +separator_flag + self.url)

    @staticmethod
    def add_article_type(article_type):
      r = get_redis()
      r.sadd('article_type_set',article_type)
      r.save()

    @staticmethod
    def get_article_type_list():
         r = get_redis()
         article_type_list = r.smembers('article_type_set')
         return article_type_list



    def save_article_to_type_detail(self):
            article_type_key = self.create_type_list_key(self.type)
            article_type_value = self.serial_to_list()
            r = get_redis()
            r.lpush(article_type_key,article_type_value)
            r.save()

    @staticmethod
    def get_article_type_detail():
        r =  get_redis()
        type_list = carticle.get_article_type_list()
        article_type_detail_list = []
        for type in type_list :
            article_type_info = carticle_type_info()
            article_type_info.type_name = type
            article_type_list_key = carticle.create_type_list_key(type)
            type_info_list = r.lrange(article_type_list_key, 0, r.llen(article_type_list_key) - 1 )
            for type_info in type_info_list:
                article_tag = ccarticle_tag()
                article_tag.title,article_tag.url = carticle.unserial_from_list(type_info )
                article_type_info.article_tag_list.append(article_tag)
            article_type_info.type_article_number = len( article_type_info.article_tag_list )
            article_type_detail_list.append(article_type_info )
        return article_type_detail_list
  

 





def getImagePath(model_instance=None):
    if model_instance is None:
        return "aaa/"
    else:
        return "%s/" % model_instance.Name

def getDescImagePath(model_instance=None):
        return "aaa/"

class myEventHander(UEditorEventHandler):
    def on_selectionchange(self):
        return """
            function getButton(btnName){
                var items=%(editor)s.ui.toolbars[0].items;
                for(item in items){
                    if(items[item].name==btnName){
                        return items[item];
                    }
                }
            }
            var btn=getButton("mybtn1");
            var selRanage=id_Description.selection.getRange()
            btn.setDisabled(selRanage.startOffset == selRanage.endOffset);

        """


class Blog(models.Model):
    title = models.CharField(u'title', max_length=480, blank=True)
    context = UEditorField(u'context', height=600, width=680, default='please enter context here...', imagePath='blog_images/', toolbars="full",
                           filePath='blog_files/', blank=True, settings={"a": 2},
                           command=[],
                               event_handler=myEventHander()
                               )


class LeaveWord(models.Model):
    leave_word_email = models.CharField(u'your email', max_length=360, blank=True)
    leave_word_context = UEditorField(u'your context', height=200, width=480, default='please enter context here...', imagePath='blog_images/', toolbars="mini",
                           filePath='blog_files/', blank=True, settings={"a": 2},
                           command=[],
                               event_handler=myEventHander()
                               )



