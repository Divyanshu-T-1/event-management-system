from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),

    path('event/<int:id>/', views.event_detail, name='event_detail'),

    # 🎓 Student registration
    path('event/<int:id>/register/', views.register_event, name='register_event'),

    # 🔥 Edit Event
    path('event/<int:id>/edit/', views.edit_event, name='edit_event'),

    # 🔥 Delete Event
    path('event/<int:id>/delete/', views.delete_event, name='delete_event'),

    path('create/', views.create_event, name='create_event'),

    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
]
