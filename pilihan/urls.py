"""pilihan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from topics import api, views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # VIEW
    url(r'^accounts/login/$', views.LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^accounts/register/$', views.RegisterView.as_view(), name='register'),
    url(r'^topic/ask/$', views.AskView.as_view(), name='ask'),
    url(r'^(?P<slug>[\w-]+)/$', views.QuestionView.as_view(), name='question'),
    url(r'^$', views.FeedView.as_view(), name='feed'),

    # API
    url(r'^question/follow/$', api.QuestionFollowView.as_view(), name='question-follower'),
    url(r'^question/downvote/$', api.QuestionDownvoteView.as_view(), name='question-downvote'),
]
