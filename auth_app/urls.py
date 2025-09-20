# backend/auth_app/urls.py
from django.urls import path, include
from rest_framework_simplejwt.views import TokenVerifyView

from .views import (
    CustomRegisterView,
    CustomPasswordResetConfirmView,
    CustomTokenObtainPairView,
    CustomOAuthRegisterOrLoginView,
    CustomPasswordResetView,
    DeleteUserView,
    CustomVerifyEmailView,
    RefreshTokenView,
    update_points,
    get_user_data,
    update_name,
)

urlpatterns = [
    # Кастомные пути
    path('registration/verify-email/', CustomVerifyEmailView.as_view(), name='custom_verify_email'),
    path('registration/', CustomRegisterView.as_view(), name='custom_register'),
    path('custom/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('custom/oauth/register-or-login/', CustomOAuthRegisterOrLoginView.as_view(), name='oauth_register_or_login'),  #  OAuth Google NextAuth
    
    path("refresh/", RefreshTokenView.as_view(), name="token_refresh"),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Сброс пароля
    path('password/reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password/reset/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    # Удаление по id или email
    path('delete-user/<int:id>/', DeleteUserView.as_view(), name='delete_user_by_id'),
    path('delete-user/', DeleteUserView.as_view(), name='delete_user_by_email'),  # Удаление по email

    # Стандартные пути аутентификации
    path('', include('dj_rest_auth.urls')),  # стандартные пути dj-rest-auth
    
    # API пользователя
    path('update-points/', update_points, name='update-points'),    # Добавление очков пользователю 
    path('get-user-data/', get_user_data, name='get-user-data'),    # Получение данных о пользователе 
    path('update-name/', update_name, name='update-name'),          # Обновление имени
]

