"""VueWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from users.views import index
from .settings import *
from users import urls

# 1. Setup urlpatterns
urlpatterns = [
    path('', index),                                    # User Site : Home
    path('admin/', admin.site.urls),                    # Admin Site
    path('users/', include('users.urls')),              # User Site : [users]
]
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)

# 2. AdminSite attributes 설정 : 2021.03.05
admin.site.site_header = '사이트 헤더'
admin.site.site_title = 'SC-Admin Site'
admin.site.index_title = 'SC Project'
