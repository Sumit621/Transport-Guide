from django.contrib import admin
from django.urls import path, include
from tg import views

urlpatterns = [
    path('',views.loginUser,name="login"),
    path('index',views.index,name="index"),
    path('login',views.loginUser,name="login"),
    path('logout',views.logoutUser,name="logout"),
    path('signup',views.signupUser,name="signup"),
    path('viewRoute',views.viewRoute,name="viewRoute"),
    path('viaPlace',views.viaPlace,name="viaPlace"),
    path('viewHistory',views.viewHistory,name="viewHistory"),
    path('viewPoribohon',views.viewPoribohon,name="viewPoribohon"),
    path('modPrefs',views.modPrefs,name="modPrefs"),
    path('nearestHub',views.nearestHub,name="nearestHub"),
    path('busReview',views.busReview,name="busReview"),
    path('adminIndex',views.adminIndex,name="adminIndex"),
    path('statisticsPage',views.statisticsPage,name="statisticsPage"),
    path('viewLogs',views.viewLogs,name="viewLogs"),
    path('viewSignInOut',views.viewSignInOut,name="viewSignInOut"),
    path('DataBusRoutes',views.DataBusRoutes,name="DataBusRoutes"),
    path('AddBusRoutes',views.AddBusRoutes,name="AddBusRoutes"),
    path('DataPoribohonRoutes',views.DataPoribohonRoutes,name="DataPoribohonRoutes"),
    path('AddPoribohonRoutes',views.AddPoribohonRoutes,name="AddPoribohonRoutes"),
    path('DataUserPrefs',views.DataUserPrefs,name="DataUserPrefs"),
    path('AddUserPrefs',views.AddUserPrefs,name="AddUserPrefs"),
    path('DataPlaceLocs',views.DataPlaceLocs,name="DataPlaceLocs"),
    path('AddPlaceLocs',views.AddPlaceLocs,name="AddPlaceLocs"),
    path('DataHubLocs',views.DataHubLocs,name="DataHubLocs"),
    path('AddHubLocs',views.AddHubLocs,name="AddHubLocs"),
    
]