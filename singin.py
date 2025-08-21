import requests
import schedule
import time

# ====== 配置区 ======
EMAIL = "你的网易云邮箱"
PASSWORD = "你的密码"

API_URL = "https://neteasecloudmusicapi.vercel.app"  # 别人部署好的API
session = requests.Session()


def login():
    """邮箱登录"""
    url = f"{API_URL}/login"
    params = {
        "email": EMAIL,
        "password": PASSWORD
    }
    resp = session.get(url, params=params)
    data = resp.json()
    if data.get("code") == 200:
        print("登录成功:", data.get("profile", {}).get("nickname", ""))
    else:
        print("登录失败:", data)
        raise Exception("Login failed")


def sign_in():
    """每日签到"""
    url = f"{API_URL}/daily_signin"
    resp = session.post(url, params={"type": 0})  # 0=安卓端签到，1=PC端签到
    data = resp.json()
    if data.get("code") == 200:
        print("签到成功:", data.get("point", "获得积分"))
    elif data.get("code") == -2:
        print("今天已经签到过了")
    else:
        print("签到失败:", data)


def job():
    try:
        login()
        sign_in()
    except Exception as e:
        print("执行任务失败:", e)


if __name__ == "__main__":
    # 每天早上 8 点执行一次
    schedule.every().day.at("08:00").do(job)

    print("自动签到程序已启动...")
    while True:
        schedule.run_pending()
        time.sleep(60)
