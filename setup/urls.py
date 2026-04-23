from django.contrib import admin
from django.urls import path
from hardware import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('montagem/', views.simular_montagem, name='simular_montagem'),
    path('minhas-montagens/', views.minhas_montagens, name='minhas_montagens'), # <-- NOVA ROTA!
]