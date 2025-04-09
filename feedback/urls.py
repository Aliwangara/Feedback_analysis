from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('submit/', views.submit_feedback, name='submit_feedback'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('fetch-twitter/', views.fetch_twitter_view, name='fetch_twitter'),
    path('fetch-reddit/', views.fetch_reddit, name='fetch_reddit'),

    path('statistics_report/',views.statistics_report, name='statistics_report'),



    path('comments/', views.all_comments, name='all_comments'),


]