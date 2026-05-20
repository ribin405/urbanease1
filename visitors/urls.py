from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.create_visitor_request, name='create_visitor_request'),
    path('success/', views.success_page, name='success_page'),
]