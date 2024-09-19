import json
import os
import re

import requests

issue_body = os.getenv("ISSUE_BODY")

category_mapping = {
    "社交平台": "social",
    "新闻媒体": "news",
    "博客": "blogs",
    "技术网站": "technology",
    "设计与创意": "design",
    "在线教育": "education",
    "电商平台": "ecommerce",
    "影视与视频": "movies",
    "音乐与播客": "music",
    "游戏": "gaming",
    "论坛与社区": "forums",
    "科技产品更新": "tech",
    "学术期刊": "academic",
    "体育赛事": "sports",
    "旅行与出行": "travel",
    "金融与投资": "finance",
    "政务与通知": "government",
    "其他": "others",
}


def extract_issue_input(body):
    patterns = {
        "site_url": r"官方网站地址\s*：?\s*(https?://\S+)",
        "rss_url": r"三方 RSS 地址\s*：?\s*(https?://\S+)",
        "rss_description": r"三方 RSS 使用说明\s*：?\s*(.*?)\s*$",
        "category": r"网站类型\s*：?\s*(.*)",
    }
    matches = {
        key: re.search(pattern, body, re.DOTALL) for key, pattern in patterns.items()
    }
    if any(match is None for match in matches.values()):
        return None, None, None, None
    return (
        matches["site_url"].group(1).strip(),
        matches["rss_url"].group(1).strip(),
        matches["rss_description"].group(1).strip(),
        matches["category"].group(1).strip(),
    )


def check_url_accessibility(url):
    try:
        requests.get(url, timeout=10)
        return True
    except requests.exceptions.RequestException:
        return False


def update_json_file(category, site_url, rss_url, rss_description):
    file_path = "routes.json"
    data = []
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                pass
    entry = {
        "category": category,
        "site_url": site_url,
        "rss_url": rss_url,
        "rss_description": rss_description,
    }
    data.append(entry)
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def main():
    site_url, rss_url, rss_description, category = extract_issue_input(issue_body)
    if not all([site_url, rss_url, rss_description, category]):
        print("必要的字段缺失，请确保所有信息填写完整。")
        return
    if not check_url_accessibility(site_url):
        print(f"警告：{site_url} 无法访问，但继续处理。")
    if not check_url_accessibility(rss_url):
        print(f"错误：{rss_url} 无法访问。")
        return
    update_json_file(category, site_url, rss_url, rss_description)
    print(f"成功更新 routes.json 文件。")


if __name__ == "__main__":
    main()
