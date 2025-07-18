import sys
import json

def clean_repeated_alerts(alerts):
    if not alerts:
        return alerts
    
    cleaned = [alerts[0]]  # Keep the first alert
    
    for current_alert in alerts[1:]:
        last_alert = cleaned[-1]
        
        # Keep alert if it's different from the previous one
        if current_alert["alert"] != last_alert["alert"]:
            cleaned.append(current_alert)
    
    return cleaned

alerts_file_path = sys.argv[1]

# Load alerts
with open(alerts_file_path, "r") as f:
    alerts = json.load(f)

print(f"Original alerts: {len(alerts)}")

# Clean repeated alerts
cleaned_alerts = clean_repeated_alerts(alerts)

print(f"Cleaned alerts: {len(cleaned_alerts)}")
print(f"Removed {len(alerts) - len(cleaned_alerts)} repeated alerts")

# Save back to the same file
with open(alerts_file_path, "w") as f:
    json.dump(cleaned_alerts, f, indent=2)

print(f"Alerts cleaned and saved to {alerts_file_path}")

"""
Examples:
uv run python 04_clean_alerts.py "processed/1gi5qn1khVk_15_alerts.json"
uv run python 04_clean_alerts.py "processed/IDN4S-mhplk_21_alerts.json"
uv run python 04_clean_alerts.py "processed/KTDen9ooazo_22_alerts.json"
uv run python 04_clean_alerts.py "processed/ms-Q3t5IqNM_12_alerts.json"
uv run python 04_clean_alerts.py "processed/p_sOLAtXY44_28_alerts.json"
uv run python 04_clean_alerts.py "processed/V3QMrftx3cQ_32_alerts.json"
"""