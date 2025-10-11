# chat_app/model_providers/openrouter/query.py
import requests
from decouple import config
from django.core.cache import cache
from django.conf import settings
from .selector import get_top_models

OPENROUTER_API_KEY = config("OPENROUTER_API_KEY")
OPENROUTER_URL = config("OPENROUTER_API_URL")


def query_openrouter(
    prompt: str,
    model_id: str,
    language: str = "en",
    system_prompt: str = None,
    temperature: float = 0.7,
):
    print("prompt", prompt, "model_id", model_id)
    print(
        "language", language, "system_prompt", system_prompt, "temperature", temperature
    )
    """Обновлённая версия с поддержкой кастомных параметров"""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": settings.FRONT_URL,
        "X-Title": "AI Chat Demo",
    }

    payload = {
        "model": model_id,
        "messages": [
            {
                "role": "system",
                "content": system_prompt or "You are a helpful assistant.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
    }

    try:
        response = requests.post(
            OPENROUTER_URL, headers=headers, json=payload, timeout=30
        )
                
        # сразу перед response.raise_for_status()
        print("[OR] status:", response.status_code)
        try:
            data = response.json()
            # ключи верхнего уровня
            # print("[OR] top keys:", list(data.keys()))
            # ключи первого choice
            if data.get("choices"):
                # print("[OR] choice[0] keys:", list(data["choices"][0].keys()))
                # что внутри message / content
                msg = data["choices"][0].get("message", {})
                # print("[OR] message keys:", list(msg.keys()) if isinstance(msg, dict) else type(msg))
                # покажем первые 200 символов «контента» (где бы он ни лежал)
                content_preview = (
                    (msg.get("content") if isinstance(msg, dict) else None)
                    or data["choices"][0].get("content")
                    or ""
                )
                # print("[OR] content preview:", str(content_preview)[:200].replace("\n", " "))
            else:
                print("[OR] no choices in payload!")
        except Exception as jerr:
            # если не JSON — выведем голый текст начала ответа
            print("[OR] non-JSON response:", repr(response.text[:400]))
            raise jerr         
        
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return content, model_id

    except Exception as e:
        print(f"Ошибка запроса: {str(e)}")
        try:
            # если сервер всё же вернул json с описанием — покажем
            print("[OR][error] body:", getattr(e, "response", None) and e.response and e.response.text[:400])
        except Exception:
            pass
        # Обновляем кэш моделей
        fresh_models = get_top_models()

        # Берём первую доступную модель
        fallback_model = fresh_models["text_models"][0]["model_id"]
        print("fallback_model", fallback_model)
        try:
            # Повторный запрос
            response = requests.post(
                OPENROUTER_URL,
                headers=headers,
                json={**payload, "model": fallback_model},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"], fallback_model

        except Exception as e:
            print(f"Вторая ошибка от fallback_model: {str(e)}")
            # Формируем сообщение в зависимости от языка
            error_msg = (
                "OpenRouter сейчас недоступен. Пожалуйста, попробуйте позже."
                if language == "ru"
                else "OpenRouter is currently unavailable. Please try again later."
            )
            return error_msg, None
