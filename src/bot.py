import os
import requests
def enviar_alerta_teams(valor_aqi: float | str, ubicacion: str, estado_txt: str, color_card: str) -> None:
    """
    Docstring para enviar_alerta_teams
    
    :param valor_aqi: El valor de la calidad del aire (sin procesar, es decir, en una escala del 1 al 5)
    :type valor_aqi: float | str
    :param ubicacion: En donde esta el dispositivo
    :type ubicacion: str
    :param estado_txt: 🚨 PELIGRO: Calidad mala (solo se llama a esta funcion si es mala la calidad)
    :type estado_txt: str
    :param color_card: Attention (es para que el texto salga en color rojo)
    :type color_card: str
    """
    url = os.getenv("WEBHOOK_TEAMS")
    url_dashboard = os.getenv("DASHBOARD_URL")
    payload = {
        "type": "message",
        "attachments": [{
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "type": "AdaptiveCard",
                "version": "1.4",
                "body": [
                    {
                        "type": "TextBlock", 
                        "text": f"{estado_txt}", 
                        "color": color_card, 
                        "weight": "Bolder", 
                        "size": "Large"
                    },
                    {
                        "type": "TextBlock", 
                        "text": f"📍 Ubicación: {ubicacion}", 
                        "weight": "Bolder",
                        "separator": True
                    },
                    {
                        "type": "FactSet", 
                        "facts": [
                            {"title": "Estado Actual:", "value": f"{valor_aqi} (AQI)"},
                            {"title": "Pronóstico (30m):", "value": "🚨 NIVELES CRÍTICOS DETECTADOS"}
                        ]
                        }
                ],
                "actions": [{"type": "Action.OpenUrl", "title": "Ver Dashboard General", "url": url_dashboard}]
            }
        }]
    }
    requests.post(url, json=payload)