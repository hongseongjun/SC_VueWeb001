from django.urls import path, include
from . import views

# 1. [app_name] 설정
app_name = 'users'

# 2. [urlpatterns] 설정
urlpatterns = [
    # 1) 사이트 홈/메인 페이지 및 로그-인/아웃 페이지 관리
    path('', views.index),                                                          #사이트 홈페이지
    #path('main/', views.main_view, name='main'),                                    #사이트 메인 페이지(로그인 상태)
    #path('login/', views.LoginView.as_view(), name='login'),                        #로그인
    #path('logout/', views.logout_view, name='logout'),                              #로그아웃
]
