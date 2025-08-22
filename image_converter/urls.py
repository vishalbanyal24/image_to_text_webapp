from django.urls import path
from . import views

urlpatterns = [
    path('', views.convert_image_to_text, name='convert_image_to_text'),
]
