# encoding:utf-8
import os
import sys
import json
import requests
from datetime import datetime, timezone, timedelta

# Prefer HTTPS for stability
PUSHPLUS_API = "https://www.pushplus.plus/send"
BEIJING_TZ = timezone(timedelta(hours=8))


def send_notification(token, title, content, template="markdown"):
    data = {
        "token": token,
        "title": title,
        "content": content,
        "template": template,
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(
            PUSHPLUS_API,
            data=json.dumps(data).encode("utf-8"),
            headers=headers,
            timeout=30,
        )
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"推送请求失败: {e}")
        # Best-effort: surface response body if available
        if getattr(e, "response", None) is not None:
            try:
                print("响应内容:", e.response.text)
            except Exception:
                pass
        return {"code": -1, "msg": str(e)}

    try:
        result = response.json()
    except ValueError:
        # Non-JSON response
        print("推送失败: 返回不是 JSON")
        print("HTTP 状态码:", response.status_code)
        print("响应内容:", response.text)
        return {"code": -2, "msg": "non-json response", "status": response.status_code}

    if result.get("code") == 200:
        print(f"推送成功: {title}")
    else:
        print(f"推送失败: {result.get('msg')}")
    return result


def main():
    token = os.environ.get("PUSHPLUS_TOKEN")
    if not token:
        print("错误: 未设置 PUSHPLUS_TOKEN")
        sys.exit(1)

    now = datetime.now(BEIJING_TZ)
    title = f"每日通知 - {now.strftime('%m月%d日')}"

    # ===== 固定文案（可自行修改） =====
    # NOTE: 之前这里的三引号字符串被截断（出现 [...]/乱码），会导致 Python 语法错误。
    # 现在改成一段完整的固定文案，确保脚本可运行。
    content = (
        "## 你今天已经做的很好了\n\n"
        "不必在意其他人的评价看法，你有你自己的评价体系。\n"
        "未来的辉煌，过去的挫折，都与你无关。\n\n"
        "深呼吸，平静下来。\n"
    )

    send_notification(token, title, content)


if __name__ == "__main__":
    main()
