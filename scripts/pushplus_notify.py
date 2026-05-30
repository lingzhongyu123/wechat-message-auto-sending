# encoding:utf-8
import os
import sys
import json
import requests
from datetime import datetime, timezone, timedelta

PUSHPLUS_API = "http://www.pushplus.plus/send"
BEIJING_TZ = timezone(timedelta(hours=8))


def send_notification(token, title, content, template="markdown"):
    data = {
        "token": token,
        "title": title,
        "content": content,
        "template": template,
    }
    headers = {"Content-Type": "application/json"}
    body = json.dumps(data).encode("utf-8")
    response = requests.post(PUSHPLUS_API, data=body, headers=headers, timeout=30)
    result = response.json()
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

    # ===== 在这里修改你的推送内容 =====
    content = f"""## 你今天已经做的很好了，不必在意其他人的评价看法，你有你自己的评价体系，未来的辉煌，过去的挫折，都与你无关，深呼吸，平静下来，别刷知乎或抖音了，现在你没啥可以想的了，没事哒没事哒，好好睡觉吧
"""

    send_notification(token, title, content)


if __name__ == "__main__":
    main()
