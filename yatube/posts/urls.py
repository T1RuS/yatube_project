from django.urls import path
from . import views


app_name = 'posts'

urlpatterns = [
    path('', views.index, name='main_page'),
    path('groups/<slug:pk>/', views.group_posts, name='group_list'),
]
