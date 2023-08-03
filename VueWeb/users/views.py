from django.shortcuts import render

# Create your views here.
# 1. 메인화면(로그인 전)

def index(request):
    return render(request, 'users/index.html')