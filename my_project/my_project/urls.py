"""my_project URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from views import signup_view,Login_view,post_view,feed_view,like_view,comment_view
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url('^admin/', admin.site.urls),

    url('post/',post_view),

    url('like/', like_view),
    url('comment/', comment_view),
    url('feed/', feed_view),
    url('login/', Login_view),
    url('',signup_view),
]
