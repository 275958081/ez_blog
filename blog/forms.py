from django import forms
from  DjangoUeditor.widgets import UEditorWidget
from  DjangoUeditor.forms import UEditorField, UEditorModelForm
from models import Blog,LeaveWord


class BlogUEditorForm(forms.Form):
    blog_title = forms.CharField(label=u'title')
    blog_context = forms.CharField(label=u"context",
                              widget=UEditorWidget({"width":600, "height":500, "imagePath":'blog_images', "filePath":'blog_file', "toolbars":"full"}))


    #BlogUEditorModelForm
class AddBlogTypeForm(forms.Form):
    article_type = forms.CharField(label =u'article_type')


class BlogUEditorModelForm(UEditorModelForm):
    class Meta:
        model = Blog



class LeaveWordModelForm(UEditorModelForm):
    class Meta:
        model = LeaveWord
 
         