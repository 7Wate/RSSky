import json
import os
import re

import requests

issue_body = os.getenv("ISSUE_BODY")
issue_number = os.getenv("ISSUE_NUMBER")
repo_name = os.getenv("GITHUB_REPOSITORY")
github_token = os.getenv("GITHUB_TOKEN")

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


def send_issue_comment(issue_number, comment):
    """发送评论到 Issue"""
    url = f"https://api.github.com/repos/{repo_name}/issues/{issue_number}/comments"
    headers = {"Authorization": f"Bearer {github_token}"}
    data = {"body": comment}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 201:
        print(f"Oops! 无法发送评论到 Issue: {response.text}")
    else:
        print(f"🎉 评论已成功发送到 Issue #{issue_number}!")


def close_issue(issue_number):
    """关闭 Issue"""
    url = f"https://api.github.com/repos/{repo_name}/issues/{issue_number}"
    headers = {"Authorization": f"Bearer {github_token}"}
    data = {"state": "closed"}
    response = requests.patch(url, json=data, headers=headers)
    if response.status_code != 200:
        print(f"Oops! 无法关闭 Issue: {response.text}")
    else:
        print(f"✅ Issue #{issue_number} 已成功关闭!")


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


def route_exists_in_json(key):
    file_path = "routes/routes.json"
    if not os.path.exists(file_path):
        return False
    with open(file_path, "r") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            return False
    for entry in data:
        if entry["key"] == key:
            return True
    return False


def route_exists_in_markdown(category, site_url):
    category_slug = category_mapping.get(category, "others")
    category_md_path = f"docs/routes/{category_slug}.md"
    if not os.path.exists(category_md_path):
        return False
    with open(category_md_path, "r") as file:
        content = file.read()
    return site_url in content


def update_json_file(key, value):
    file_path = "routes/routes.json"
    data = []
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                pass
    entry = {
        "key": key,
        "value": value,
    }
    data.append(entry)
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
    return file_path


def update_markdown_file(category, site_url, rss_url, rss_description):
    category_slug = category_mapping.get(category, "others")
    category_md_path = f"docs/routes/{category_slug}.md"
    md_content = f"""
## {site_url}

- **RSS URL**: [{rss_url}]({rss_url})
- **Description**: {rss_description}

---
"""
    with open(category_md_path, "a") as category_md:
        category_md.write(md_content)
    print(f"📄 Updated {category_md_path} with new RSS route for {category}.")


def main():
    site_url, rss_url, rss_description, category = extract_issue_input(issue_body)

    if not all([site_url, rss_url, rss_description, category]):
        send_issue_comment(issue_number, "⚠️ 必要的字段缺失，请确保所有信息填写完整。")
        return

    if not check_url_accessibility(site_url):
        send_issue_comment(issue_number, f"⚠️ 警告：{site_url} 无法访问，但继续处理。")

    if not check_url_accessibility(rss_url):
        send_issue_comment(issue_number, f"❌ 错误：{rss_url} 无法访问。")
        return

    key = f"{category}/{site_url}"
    if route_exists_in_json(key) or route_exists_in_markdown(category, site_url):
        send_issue_comment(
            issue_number,
            f"⚠️ 路由已存在于 routes.json 或对应的 Markdown 文档中，请人工手动处理。",
        )
        return

    file_path = update_json_file(key, rss_url)
    update_markdown_file(category, site_url, rss_url, rss_description)
    send_issue_comment(
        issue_number, f"🎉 成功更新了 routes.json 文件，并记录了新路由。"
    )
    close_issue(issue_number)

    print(f"🎉 成功更新 {file_path} 文件，并关闭了 Issue #{issue_number}。")


if __name__ == "__main__":
    main()
