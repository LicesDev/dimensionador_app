from django.urls import path
from . import views

urlpatterns = [
    path('video_feed/', views.video_feed, name='video_feed'),
    path('sse/', views.sse_view, name='sse_view'),  # Asegúrate de que esta línea esté presente
]