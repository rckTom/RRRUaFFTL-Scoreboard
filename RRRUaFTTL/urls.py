"""RRRUaFTTL URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from scoreboard.forms import LoginForm, MyPasswordChangeForm

urlpatterns = [
    url(r'^', include('scoreboard.urls')),
    url(r'^scoreboard/', include('scoreboard.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/',views.login ,{'template_name': 'login.html','authentication_form':LoginForm}),
    url(r'^logout/',views.logout,{'next_page': '/'}),
    url(r'^change_password/',views.password_change,{'template_name': 'change_password.html','password_change_form':MyPasswordChangeForm,'post_change_redirect':'/'}),
    url(r'^password_change_done/',views.password_change_done,{'template_name':'thanks.html'})]
