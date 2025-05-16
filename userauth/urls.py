from django.urls import path
from userauth import views

urlpatterns = [
    # Urls related to login and auth methods
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('refresh-token/', views.refresh_token_view, name='refresh-token'),
]
