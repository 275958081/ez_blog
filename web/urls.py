from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
import blog
import settings
from blog.views import  BlogUEditorModelForm,ajaxcmd
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^ueditor/',include('DjangoUeditor.urls')),
     url('^$', 'blog.views.lp_main'),
     url('^add_article$', 'blog.views.add_article'),
     url('^logout$', 'blog.views.logout'),
     url('^login$', 'blog.views.login'),
     url('^blog_index_(\d{1,3})$', 'blog.views.read_blog'),
     url('^article_(\d{1,3})$', 'blog.views.read_article'),
      url('^article_(\d{1,3})_editor$', 'blog.views.edit_article'),
     url('^add_article_type$', 'blog.views.add_article_type'),
     url(r'^ajaxcmd/$','blog.views.ajaxcmd'),

    # url(r'^web/', include('web.web.urls')),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
        url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
        url(r'^(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
    )
