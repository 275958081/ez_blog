 # -*- coding: utf-8 -*-
from blog import models

css_and_js_render_part = u"""
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>燃木的个博客</title>
<link href="http://libs.baidu.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">
<script src="http://libs.baidu.com/jquery/2.0.0/jquery.min.js"></script>
<script src="http://libs.baidu.com/bootstrap/3.0.3/js/bootstrap.min.js"></script>
<link href="/static/css/styles.css" rel="stylesheet">
<link href="/static/css/animation.css" rel="stylesheet">
<!-- 返回顶部调用 begin -->
<link href="/static/css/lrtk.css" rel="stylesheet" />
<script type="text/javascript" src="/static/js/jquery.js"></script>
<script type="text/javascript" src="/static/js/js.js"></script>

<!-- 返回顶部调用 end-->
<!--[if lt IE 9]>
<script src="js/modernizr.js"></script>
<![endif]-->

"""


blog_view_css_and_js_render = u"""
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>燃木的个博客</title>
<link href="/static/css/styles.css" rel="stylesheet">
<link href="/static/css/view.css" rel="stylesheet">
<!-- 返回顶部调用 begin -->
<link href="/static/css/lrtk.css" rel="stylesheet" />
<script type="text/javascript" src="/static/js/jquery.js"></script>
<script type="text/javascript" src="/static/js/js.js"></script>
<!-- 返回顶部调用 end-->
<!--[if lt IE 9]>
<script src="js/modernizr.js"></script>
<![endif]-->
"""


header_part = u"""
<header>
  <nav id="nav">
    <ul>
      <li><a href="/" >网站首页</a></li>
      <li><a href="/web/" target="_blank" title="个人相册">相册</a></li>
      <li><a href="/newshtml5/" target="_blank" title="加入<it人在深圳>的部落">it人在深圳</a></li>
      <li><a href="/godtime" target="_blank" title="流金岁月">流金岁月</a></li>
	  <li><a href="/godtime" target="_blank" title="流金岁月"><button type="button">登陆 </button></a></li>
	  
    </ul>
    <script src="js/silder.js"></script><!--获取当前页导航 高亮显示标题--> 
  </nav>
</header>

"""

header_part_1 =u"""
<nav class="navbar navbar-inverse" role="navigation">
   <div>  
      <button type="button" class="btn btn-inverse navbar-btn">
         <a href="/" >网站首页</a>
      </button>
 
      <button type="button" class="btn btn-inverse navbar-btn">
         <a href="/web/" target="_blank" title="个人相册">相册</a>
      </button>
  
      <button type="button" class="btn btn-inverse navbar-btn">
         <a href="/newshtml5/" target="_blank" title="加入<it人在深圳>的部落">it人在深圳</a>
      </button>
  
      <button type="button" class="btn btn-inverse navbar-btn">
         <a href="/godtime" target="_blank" title="流金岁月">流金岁月</a>
      </button>
   </div>
</nav>
"""

def get_toatl_blog_list(n):
	s = u"""
      <div class="clicks">
        <h2>博文列表</h2>
        <ol>"""
	l = models.cblog.get_totao_blog_list(n)
	for blog_tag in l:
		s.append(u"<li><span><a href=\"")
		s.append(blog_tag.url)
		s.append(u"\">")
		s.append(blog_tag.titel)
		s.append(u"</a></span></li>")
    
	s.append(u"</ol></div>")




