# payment/urls.py
from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    # Первый платеж
    path('process-kassa/', views.process_kassa, name='process_kassa'),
    # Вэбхуки от Кассы waiting_for_capture, succeeded, canceled, refund
    path('webhook-kassa/', views.kassa_webhook, name='kassa_webhook'),
    # Подтверждение платежа
    path('confirm-payment/', views.confirm_payment, name='confirm_payment'),
    # Повторный платеж Подписки по исходному первому платежу
    path('process-recurring-payment/', views.process_recurring_payment, name='process_recurring_payment'),
    # Возврат платежа
    path('refund/', views.process_refund, name='process_refund'),
    # Валидация купона
    path('validate-coupon/', views.validate_coupon, name='validate_coupon'),
    # Подписки
    path('charge-subscriptions/', views.charge_subscriptions_http, name='charge_subscriptions_http'),
    # Отписка
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
]
