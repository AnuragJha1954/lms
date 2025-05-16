from django.urls import path
from v1 import views

urlpatterns = [
    #Content management related Urls
    path('content/<int:content_id>/complete/', views.mark_content_completed, name='mark-content-completed'),
]
