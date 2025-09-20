# backend/backend/urls.py
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/auth/', include('auth_app.urls')),  # Все пути auth перенесены в auth_app.urls
    path('accounts/', include('allauth.urls')),  # Пути для верификации email   
    path('api/chat/', include('chat_app.urls')),  # Все пути chat перенесены в chat_app.urls
    path('healthz/', lambda request: HttpResponse("Welcome to Django REST Module!")),
]

# Добавляем только в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# cd backend
# python manage.py runserver
# cd frontend
# npm run dev

# python manage.py makemigrations
# python manage.py migrate

# python manage.py createsuperuser
# lemon@lemon.com
# 12345

# pip install -U -r requirements.txt    в проект
# pip freeze > requirements.txt         из проекта