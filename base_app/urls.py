from django.urls import path,include
from .views import home_page,user_dashboard,search_event,event_detail,api_event_list, api_event_detail, api_user_registration, api_user_registered_events,custom_login,custom_logout,custom_register,register,unregister_event

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

    #for api view
    path('api/events/', api_event_list, name='api_event_list'),
    path('api/events/<int:event_id>/', api_event_detail, name='api_event_detail'),
    path('api/events/<int:event_id>/register/', api_user_registration, name='api_user_registration'),
    path('api/user/registered-events/', api_user_registered_events, name='api_user_registered_events'),
    
]