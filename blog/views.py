# -*- coding: utf-8 -*-
# Create your views here.
#from TestApp.forms import UEditorTestModelForm,TestUEditorForm
from django.http import HttpResponse,HttpResponseRedirect,Http404,HttpResponseForbidden
from django.shortcuts import render_to_response,redirect
from blog.forms import BlogUEditorForm , BlogUEditorModelForm , AddBlogTypeForm,LeaveWordModelForm
from blog.models import carticle, cleave_word , debug_print, ccarticle_tag, carticle_type_info
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from blog.mysafe import try_login

#from TestApp.models import Blog


@csrf_protect
def login(req):
        article_type_info_list = carticle.get_article_type_detail()
        if req.method == 'POST' :
            try_login_result = try_login(req) 
            if ( try_login_result == 0 ) :
                return HttpResponseForbidden("<p>the page not found!</p>")
            elif ( try_login_result  > 0 and try_login_result <= 5 ) :
                return render_to_response( 'login.html', {'leave_try_times': try_login_result } ,context_instance = RequestContext(req) )
            else :
                is_login =  req.session.get('lp_login',False)
                pre_url = req.META.get('HTTP_REFERER','/')
                if pre_url == '/login' :
                    HttpResponseRedirect('/')
                return HttpResponseRedirect('/', locals())
        else :
            return render_to_response( 'login.html',locals(),context_instance = RequestContext(req) )
      
   


def lp_main(req):
    article_type_info_list = carticle.get_article_type_detail()
    is_login = req.session.get('lp_login',False )
    for article_type_info in article_type_info_list :
        print 'acticle type : ' , article_type_info.type_name
        for article_tag in article_type_info.article_tag_list :
            print ' url : ' , article_tag.url
            print ' title : ' , article_tag.title

    if is_login :
        print 'has login in'
    else :
        print 'not login '

    return render_to_response('base.html', locals())
   

def logout(req):
    req.session['lp_login'] = False
    print 'logout...'
    return HttpResponseRedirect(req.META.get('HTTP_REFERER','/'))



@csrf_protect
def edit_article(req,index):
    is_login =  req.session.get('lp_login',False)
    if not is_login :
        return HttpResponseRedirect('/login')
    if req.method.upper() == 'POST' :
        form = BlogUEditorModelForm(req.POST)
        if form.is_valid() :
            new_article = carticle()
            new_article.title = req.POST.get('title')
            new_article.context = req.POST.get('context')
            new_article.type      = req.POST.get('select_type')
            print 'title: ', new_article.title ,'type : ' , new_article.type
            new_article.save()
            new_article.save_article_to_type_detail()
            print 'redirect to : ' , new_article.url
            return HttpResponseRedirect(new_article.url) #return new blog's url     
        else :
            return HttpResponse(u"error data")

    else :
        article = carticle.get_article(index)  
        try :
            M = Blog.objects.get( pk =1 )
            form = BlogUEditorModelForm( instance= M )      
            form.Meta.model.title = article.title        
            form.Meta.model.context = article.context
        except:     
           form =  BlogUEditorModelForm( initial={'Description': 'test','title': article.title,'context':article.context})
           #form.Meta.model.title = article.title #
          # form.Meta.model.context = article.context
         # how push date to form ?
         
        article_type_list = carticle.get_article_type_list()
        article_type_info_list = carticle.get_article_type_detail()
        return render_to_response(u'add_article.html', locals(),
		context_instance = RequestContext(req))

    pass

@csrf_protect
def add_article(req):
    is_login =  req.session.get('lp_login',False)
    if not is_login :
        return HttpResponseRedirect('/login')
    if req.method.upper() == 'POST' :
        form = BlogUEditorModelForm(req.POST)
        if form.is_valid() :
            new_article = carticle()
            new_article.title = req.POST.get('title')
            new_article.context = req.POST.get('context')
            new_article.type      = req.POST.get('select_type')
            print 'title: ', new_article.title ,'type : ' , new_article.type
            new_article.save()
            new_article.save_article_to_type_detail()
            print 'redirect to : ' , new_article.url
            return HttpResponseRedirect(new_article.url) #return new blog's url     
        else :
            return HttpResponse(u"error data")

    else :
        print 'HttpRequest.path ',req.path
        print 'HttpRequest.path_info ' , req.path_info
        try :
            M = Blog.objects.get( pk =1 )
            form = BlogUEditorModelForm( instance= M )
        except:
           form =  BlogUEditorModelForm( initial={'Description': 'test'})

        article_type_list = carticle.get_article_type_list()
        article_type_info_list = carticle.get_article_type_detail()
        return render_to_response(u'add_article.html', locals(),
		context_instance = RequestContext(req))

def ajaxcmd(request):
    return HttpResponse(u"i come from background",content_type="plain/text")


@csrf_protect
def read_article(req,index):
    is_login =  req.session.get('lp_login',False)
    if req.method == 'POST' :
        form = BlogUEditorModelForm(req.POST)
        if form.is_valid():
            visitor_name = req.POST.get('leave_word_email')
            leave_word_context    = req.POST.get('leave_word_context')
            leave_word = cleave_word(index,visitor_name,leave_word_context)
            leave_word.save_to_db()
        else :
            HttpResponse(u"error data")

    
    article = carticle.get_article(index)
    leave_word_list = cleave_word.get_blog_leave_words(index)
    article_type_info_list = carticle.get_article_type_detail()
    
    leave_word_number = len(leave_word_list)
    try :
        M = LeaveWord.object.get( pk = 1 )
        leave_word_form = LeaveWordModelForm( instance= M )
    except :
        leave_word_form = LeaveWordModelForm( initial={'Description': 'test'} )



    return render_to_response('article_view.html', locals(), context_instance = RequestContext(req))





def god_time(req):
    return render_to_response('godtime.html',{})



@csrf_protect
def add_article_type(req):
    is_login =  req.session.get('lp_login',False)
    if not is_login :
        return HttpResponseRedirect('/login')
    if req.method == 'POST' :
        form = AddBlogTypeForm(req.POST)
        if form.is_valid() :
            new_article_type = req.POST.get('article_type')
            print new_article_type
            carticle.add_article_type(new_article_type)
            
            #return render_to_response('add_blog_type.html',{'form':form,'css_and_js':blog_view_css_and_js_render , 'header':header_part} ,context_instance=RequestContext(req))
        else :
            return HttpResponse(u"error data")

    #blog_type_list = cblog.get_type_list()
    article_type_info_list = carticle.get_article_type_detail()
    article_type_list = carticle.get_article_type_list()
    form = AddBlogTypeForm()
   
    #debug_print(blog_type_list )
    return render_to_response('add_blog_type.html', locals() ,context_instance=RequestContext(req))



