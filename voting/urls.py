from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('vote/', views.vote_view, name='vote'),
    path('logout/', views.logout_view, name='logout'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('admin-login/',views.admin_login,name='admin_login'),

]

