from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'MBTIAPP'

urlpatterns = [
    path('', views.main, name='main'),
    path('login/', auth_views.LoginView.as_view(template_name='MBTIAPP/login.html'),name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('mbtitest/', views.mbtitest, name='mbtitest'),
    path('result/', views.result, name='result'),
    path('blog/', views.blog, name='blog'),
    path('new/', views.new, name='new'),
    path('postcreate/', views.postcreate, name='postcreate'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/comment/', views.comment_create, name='comment_create'),
    path('<int:post_pk>/comment/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
]