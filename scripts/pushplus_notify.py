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
    content = f"""## 如果你正要睡觉，就别刷抖音和知乎了，没啥可以想的了，好好睡觉，然后你有自己的评价体系，慢慢来吧，没事哒，不要跟别人比较，不要去想未来如何，把今天过好就好啦"""

    send_notification(token, title, content)


if __name__ == "__main__":
    main()
