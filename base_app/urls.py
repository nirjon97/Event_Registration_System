from django.urls import path,include
from .views import home_page,user_dashboard,search_event,event_detail,custom_login,custom_logout,custom_register,register,unregister_event

urlpatterns = [
    path("",home_page,name='home_page'),
    path('<int:event_id>/', event_detail, name='event_detail'),
    path('<int:event_id>/register/', register, name='register'),
    path('<int:event_id>/unregister/', unregister_event, name='unregister_event'),
    path('custom_login/', custom_login, name='custom_login'),
    path('custom_register/', custom_register, name='custom_register'),
    path('custom_logout/', custom_logout, name='custom_logout'),
    path('search/', search_event, name='search_event'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('unregister/<int:event_id>/', unregister_event, name='unregister_event'),
    
]