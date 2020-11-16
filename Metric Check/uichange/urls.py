"""uichange URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from Metrics.views import *
from Metrics import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^$', index, name="index"),
    url(r'^index/', index, name="index"),
    url(r'^adminpage/', adminpage, name="adminpage"),
    url(r'^adminlogin/', adminlogin, name="adminlogin"),
    url(r'^adminloginentered/', adminloginentered, name="adminloginentered"),
    url(r'viewuserdata/', viewuserdata, name="viewuserdata"),
    url(r'activateuser/', activateuser, name="activateuser"),
    url(r'userdeactivate/',userdeactivate,name="userdeactivate"),
    url(r'^logout/', logout, name="logout"),
    url(r'^filedata/', filedata, name="filedata"),
    url(r'^viewfile/', viewfile, name="viewfile"),
    url(r'^findfilesloader/', findfilesloader, name="findfilesloader"),
    
    
    
    

    # url(r'^signin/', signin, name="signin"),
    # url(r'^postsignin/', postsignin, name="postsignin"),
    # # url(r'^postsignin/', views.signin()),
    # # url(r'^postsignin/', views.postsignin()),


















    url(r'^userlogincheck1/', userlogincheck1, name="userlogincheck1"),
    url(r'^userlogin/', userlogin, name="userlogin"),
    url(r'^userpage/', userpage, name="userpage"),
    url(r'^userregister/', userregister, name="userregister"),
    url(r'^uploadfile/', uploadfile, name="uploadfile"),
    url(r'^viewfildata/', viewfildata, name="viewfildata"),
    url(r'^userviewfildata/', userviewfildata, name="userviewfildata"),
    url(r'^userfiledata/', userfiledata, name="userfiledata"),

    url(r'^hai/', hai, name="hai"),
    url(r'^problems/', problems, name="problems"),

    
    url(r'^que1/', que1, name="que1"),
    url(r'^que2/', que2, name="que2"),
    url(r'^que3/', que3, name="que3"),
    url(r'^que4/', que4, name="que4"),
    url(r'^que5/', que5, name="que5"),
    url(r'^que6/', que6, name="que6"),
    url(r'^que7/', que7, name="que7"),
    url(r'^que8/', que8, name="que8"),
    url(r'^que9/', que9, name="que9"),
    url(r'^que10/', que10, name="que10"),
    
    url(r'^que11/', que11, name="que11"),
    url(r'^que12/', que12, name="que12"),
    url(r'^que13/', que13, name="que13"),
    url(r'^que14/', que14, name="que14"),
    url(r'^que15/', que15, name="que15"),
    url(r'^que16/', que16, name="que16"),
    url(r'^que17/', que17, name="que17"),
    url(r'^que18/', que18, name="que18"),
    url(r'^que19/', que19, name="que19"),
    url(r'^que20/', que20, name="que20"),

    url(r'^que21/', que21, name="que21"),
    url(r'^que22/', que22, name="que22"),
    url(r'^que23/', que23, name="que23"),
    url(r'^que24/', que24, name="que24"),
    url(r'^que25/', que25, name="que25"),
    url(r'^que26/', que26, name="que26"),
    url(r'^que27/', que27, name="que27"),
    url(r'^que28/', que28, name="que28"),
    url(r'^que29/', que29, name="que29"),
    url(r'^que30/', que30, name="que30"),
    
    url(r'^que31/', que31, name="que31"),
    url(r'^que32/', que32, name="que32"),
    url(r'^que33/', que33, name="que33"),
    url(r'^que34/', que34, name="que34"),
    url(r'^que35/', que35, name="que35"),
    url(r'^que36/', que36, name="que36"),
    url(r'^que37/', que37, name="que37"),
    url(r'^que38/', que38, name="que38"),
    url(r'^que39/', que39, name="que39"),
    url(r'^que40/', que40, name="que40"),

    url(r'^que41/', que41, name="que41"),
    url(r'^que42/', que42, name="que42"),
    url(r'^que43/', que43, name="que43"),
    url(r'^que44/', que44, name="que44"),
    url(r'^que45/', que45, name="que45"),
    url(r'^que46/', que46, name="que46"),
    url(r'^que47/', que47, name="que47"),
    url(r'^que48/', que48, name="que48"),
    url(r'^que49/', que49, name="que49"),
    url(r'^que50/', que50, name="que50"),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
