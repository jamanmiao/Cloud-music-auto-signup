import os
import requests

API_URLS = [
    "https://neteasecloudmusicapi.vercel.app",
    # 你可以在这里加更多备用 API 地址
]

EMAIL = os.environ.get("NETEASE_EMAIL")
PASSWORD = os.environ.get("NETEASE_PASSWORD")

# 检查环境变量
if not EMAIL or not PASSWORD:
    print("Error: Missing EMAIL or PASSWORD in environment variables.")
    exit(1)

session = requests.Session()

def call_api(path, method="GET", **kwargs):
    """依次尝试多个API地址，哪个通就用哪个"""
    for base in API_URLS:
        url = f"{base}{path}"
        try:
            print(f"Trying URL: {url}")  # 打印正在使用的 URL
            if method == "GET":
                r = session.get(url, timeout=15, **kwargs)
            else:
                r = session.post(url, timeout=15, **kwargs)
            return r, base
        except Exception as e:
            print(f"API request failed: {e}")
            continue
    print("Error: All API endpoints failed.")
    raise RuntimeError("All API addresses are down.")

def login():
    try:
        r, base = call_api("/login", params={"email": EMAIL, "password": PASSWORD})
        data = r.json()
        if data.get("code") == 200:
            print(f"[login] Success (API: {base}) User: {data['profile']['nickname']}")
        else:
            print(f"[login] Failed: {data}")
            exit(1)
    except Exception as e:
        print(f"[login] Error: {e}")
        exit(1)

def sign_in():
    try:
        for t in [0, 1]:  # 0=安卓端，1=PC端
            r, _ = call_api("/daily_signin", method="POST", params={"type": t})
            data = r.json()
            if data.get("code") == 200:
                print(f"[signin] Success type={t} -> +{data.get('point','')}")
            elif data.get("code") == -2:
                print(f"[signin] Already signed in today (type={t})")
            else:
                print(f"[signin] Failed type={t}: {data}")
    except Exception as e:
        print(f"[signin] Error: {e}")
        exit(1)

if __name__ == "__main__":
    login()
    sign_in()
