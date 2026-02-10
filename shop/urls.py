from django.urls import path
from . import views
urlpatterns=[
    path('',views.home,name='home'),
    path('about/',views.about_shop,name='about'),
    path('author/',views.about_author,name='author'),
]