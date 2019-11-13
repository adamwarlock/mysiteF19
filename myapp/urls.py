from django.urls import path
from myapp import views

app_name = 'myapp'

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'about', views.about, name ='about'),
    path(r'<int:book_id>', views.detail, name ='book_detail'),
    path(r'findbooks', views.findbooks, name ='findbooks'),
    path(r'place_order', views.place_order, name ='place_order'),
    path(r'review', views.review, name ='review')
    ]
