import requests

def push_to_google(record: dict, endpoint_url: str) -> tuple[bool, str]:
    if not endpoint_url:
        return False, "No endpoint URL provided."
    try:
        r = requests.post(endpoint_url, json=record, timeout=15)
        if r.status_code == 200:
            return True, "Pushed to Google Sheets."
        return False, f"HTTP {r.status_code}: {r.text[:200]}"
    except Exception as e:
        return False, str(e)
