from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('vote/', views.vote_view, name='vote'),
    path('logout/', views.logout_view, name='logout'),
]