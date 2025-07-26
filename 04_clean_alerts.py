import sys
import json
from collections import defaultdict

def get_alert_priority(alert_text):
    """Retorna nivel de prioridad: A mayor número mayor prioridad"""
    if "¡Alerta de Seguridad!" in alert_text:
        return 3
    elif "Actividad Sospechosa" in alert_text:
        return 2
    elif "Todo OK" in alert_text:
        return 1
    else:
        return 0

def group_and_prioritize_alerts(alerts):
    """Agrupa las alertas generadas en cada segundo y deja sólo la que tenga mayor prioridad"""
    grouped = defaultdict(list)
    
    for alert in alerts:
        second = int(alert["timestamp"])
        grouped[second].append(alert)
    
    prioritized = []
    for second in sorted(grouped.keys()):
        alerts_in_second = grouped[second]
        highest_priority_alert = max(alerts_in_second, key=lambda x: get_alert_priority(x["alert"]))
        prioritized.append(highest_priority_alert)
    
    return prioritized

def clean_repeated_alerts(alerts):
    """Elimina alertas duplicadas consecutivas"""
    if not alerts:
        return alerts
    
    cleaned = [alerts[0]]  # Guardar primera alerta
    
    for current_alert in alerts[1:]:
        last_alert = cleaned[-1]
        
        # Mantener alerta si es distinta de la anterior
        if current_alert["alert"] != last_alert["alert"]:
            cleaned.append(current_alert)
    
    return cleaned

video_id = sys.argv[1]

# Cargar alertas
with open(f"processed/{video_id}_alerts.json", "r") as f:
    alerts = json.load(f)

print(f"Alertas originales: {len(alerts)}")

# Paso 1: Agrupar por segundo y priorizar
prioritized_alerts = group_and_prioritize_alerts(alerts)
print(f"Luego de priorizar por segundo: {len(prioritized_alerts)}")

# Paso 2: Eliminar repetidas
cleaned_alerts = clean_repeated_alerts(prioritized_alerts)
print(f"Luego de eliminar repeticiones: {len(cleaned_alerts)}")

print(f"Total de eliminadas: {len(alerts) - len(cleaned_alerts)} alertas")

# Save back to the same file
with open(f"processed/{video_id}_alerts.json", "w") as f:
    json.dump(cleaned_alerts, f, indent=2)

print(f"Alertas limpias y guardadas en processed/{video_id}_alerts.json")

"""
Examples:
uv run python 04_clean_alerts.py "KTDen9ooazo"
uv run python 04_clean_alerts.py "1gi5qn1khVk"
uv run python 04_clean_alerts.py "IDN4S-mhplk"
uv run python 04_clean_alerts.py "ms-Q3t5IqNM"
uv run python 04_clean_alerts.py "p_sOLAtXY44"
uv run python 04_clean_alerts.py "V3QMrftx3cQ"
"""