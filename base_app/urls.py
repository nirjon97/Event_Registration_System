from django.urls import path,include
from .views import home_page,event_detail

urlpatterns = [
    path("",home_page,name='home_page'),
    path('<int:event_id>/', event_detail, name='event_detail'),
    
]