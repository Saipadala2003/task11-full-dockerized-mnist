import json
import urllib.request

API = "http://127.0.0.1:5000"
UI = "http://127.0.0.1:8501"

def get_json(url):
    with urllib.request.urlopen(url, timeout=5) as response:
        return response.status, json.loads(response.read().decode("utf-8"))

if __name__ == "__main__":
    status, payload = get_json(API + "/health")
    print("Flask /health ->", status)
    print(json.dumps(payload, indent=2))
    status, payload = get_json(API + "/")
    print("Flask / ->", status)
    print(json.dumps(payload, indent=2))
    with urllib.request.urlopen(UI + "/_stcore/health", timeout=5) as response:
        print("Streamlit /_stcore/health ->", response.status)