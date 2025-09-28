# payment/tests/test_webhooks_min.py
import json
from types import SimpleNamespace
from decimal import Decimal
import pytest
from django.contrib.auth import get_user_model
from django.test import override_settings
from payment.models import KassaPayment, Subscription, PaymentEventLog

User = get_user_model()

# Чтобы не упереться в namespace, используем прямой путь (как реально настроено в urls.py).
WEBHOOK_URL = "/api/payment/webhook-kassa/"

def make_kp(user, kassa_id="pmt-123", amount=Decimal("300.00"), sub_type="monthly"):
    """Фабрика локальной записи платежа под входящий вебхук."""
    return KassaPayment.objects.create(
        user=user,
        amount=amount,
        subscription_type=sub_type,
        coupon_code="",
        discount=0,
        status="pending",
        kassa_payment_status="waiting_for_capture",
        kassa_payment_id=kassa_id,
    )

def webhook_payload(kassa_id, kp_id, sub_type, amount="300.00", event="payment.succeeded"):
    """Ровно та структура, которую шлёт YooKassa (упрощённая под тест)."""
    return {
        "type": "notification",
        "event": event,
        "object": {
            "id": kassa_id,
            "status": "succeeded",
            "amount": {"value": amount, "currency": "RUB"},
            "metadata": {"payment_id": str(kp_id), "subscription_type": sub_type},
        },
    }

@pytest.mark.django_db
@override_settings(DJANGO_ENV="local")  # локально наш IP-чек пропускает вебхуки
def test_payment_succeeded_creates_subscription(client, monkeypatch):
    user = User.objects.create_user(email="u@test.io", password="x")
    kp = make_kp(user, kassa_id="p1", sub_type="monthly")

    # 1) пропускаем IP-чек (в реальной вьюхе он импортируется из payment.views)
    monkeypatch.setattr("payment.views.is_valid_webhook_signature", lambda req: True)

    # 2) мок YooKassa SDK на find_one: вернём объект с сохранённым способом оплаты
    fake_remote = SimpleNamespace(payment_method=SimpleNamespace(id="pm-1", saved=True), status="succeeded")
    monkeypatch.setattr("payment.hooks.KPayment.find_one", lambda _id: fake_remote)

    # 3) мок update_payment_status: помечаем платёж как успешный, имитируем то, что делает утилита
    def _stub_update(payment_id, remote):
        obj = KassaPayment.objects.get(kassa_payment_id=payment_id)
        obj.kassa_payment_status = "succeeded"
        obj.status = "completed"
        obj.income_amount = obj.amount
        obj.save(update_fields=["kassa_payment_status", "status", "income_amount", "updated_at"])
        return True
    monkeypatch.setattr("payment.hooks.update_payment_status", _stub_update)

    payload = webhook_payload("p1", kp.id, "monthly", amount="300.00")
    resp = client.post(WEBHOOK_URL, data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 200

    # Проверяем запись платежа
    kp.refresh_from_db()
    assert kp.kassa_payment_status == "succeeded"
    assert kp.status == "completed"

    # Создана/обновлена подписка
    sub = Subscription.objects.filter(user=user, plan="monthly", status="active").first()
    assert sub is not None
    assert sub.payment_method_id == "pm-1"
    assert sub.next_charge_at is not None

    # Записан журнал события
    log = PaymentEventLog.objects.filter(event_id="p1", event_type="payment.succeeded", applied=True).first()
    assert log is not None

@pytest.mark.django_db
@override_settings(DJANGO_ENV="local")
def test_payment_succeeded_is_idempotent(client, monkeypatch):
    user = User.objects.create_user(email="u2@test.io", password="x")
    kp = make_kp(user, kassa_id="p2", sub_type="monthly")

    monkeypatch.setattr("payment.views.is_valid_webhook_signature", lambda req: True)
    fake_remote = SimpleNamespace(payment_method=SimpleNamespace(id="pm-2", saved=True), status="succeeded")
    monkeypatch.setattr("payment.hooks.KPayment.find_one", lambda _id: fake_remote)

    def _stub_update(payment_id, remote):
        obj = KassaPayment.objects.get(kassa_payment_id=payment_id)
        obj.kassa_payment_status = "succeeded"
        obj.status = "completed"
        obj.save(update_fields=["kassa_payment_status", "status", "updated_at"])
        return True
    monkeypatch.setattr("payment.hooks.update_payment_status", _stub_update)

    body = json.dumps(webhook_payload("p2", kp.id, "monthly"))

    # Первый раз
    assert client.post(WEBHOOK_URL, data=body, content_type="application/json").status_code == 200
    # Дубликат того же события
    assert client.post(WEBHOOK_URL, data=body, content_type="application/json").status_code == 200

    # Подписка одна (не размножилась)
    assert Subscription.objects.filter(user=user, plan="monthly").count() == 1
    # Журналы события есть на оба вызова
    assert PaymentEventLog.objects.filter(event_id="p2", event_type="payment.succeeded").count() == 2

@pytest.mark.django_db
@override_settings(DJANGO_ENV="prod")  # в прод-режиме IP-чек включён
def test_webhook_rejected_by_ip_check(client):
    # Без monkeypatch'а вебхук должен быть отрезан сразу по IP
    payload = {"type": "notification", "event": "payment.succeeded", "object": {"id": "x"}}
    resp = client.post(WEBHOOK_URL, data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 403
    # И в журнал его не пишем (лог пишется только после IP-чека)
    assert PaymentEventLog.objects.count() == 0
