# events/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/register/', views.register_event, name='register_event'),
    path('event/<int:event_id>/payment/', views.create_payment, name='create_payment'),
    path('event/<int:event_id>/unregister/', views.unregister_event, name='unregister_event'),
    path('event/<int:event_id>/registrations/', views.registration_list, name='registration_list'),
    path('upload/', views.upload_event, name='upload_event'),
    path('event/<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),
    path('event/<int:event_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.custom_logout, name='logout'),
]