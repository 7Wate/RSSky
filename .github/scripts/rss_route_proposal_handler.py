import json
import os
import re

import requests

issue_body = os.getenv("ISSUE_BODY")

# 定义简化后的分类
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
    site_url_match = re.search(r"官方网站地址\s*：?\s*(https?://\S+)", body)
    rss_url_match = re.search(r"三方 RSS 地址\s*：?\s*(https?://\S+)", body)
    rss_description_match = re.search(
        r"三方 RSS 使用说明\s*：?\s*(.*?)\s*$", body, re.DOTALL
    )
    category_match = re.search(r"网站类型\s*：?\s*(.*)", body)

    if (
        not site_url_match
        or not rss_url_match
        or not rss_description_match
        or not category_match
    ):
        return None, None, None, None

    site_url = site_url_match.group(1).strip()
    rss_url = rss_url_match.group(1).strip()
    rss_description = rss_description_match.group(1).strip()
    category = category_match.group(1).strip()

    return site_url, rss_url, rss_description, category


def check_url_accessibility(url):
    try:
        response = requests.get(url, timeout=10)
        return True
    except requests.exceptions.RequestException:
        return False


def generate_key_from_url(url):
    return "/".join(url.split(".")[::-1])


def update_json_file(domain, key, value):
    file_path = f"routes/{domain}.json"
    data = []

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                pass

    existing_entry = next((entry for entry in data if entry["key"] == key), None)
    if existing_entry:
        existing_entry["value"] = value
    else:
        data.append({"key": key, "value": value})

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def create_or_update_markdown(domain, category, site_url, rss_url, rss_description):
    # 获取分类的简化名称
    category_slug = category_mapping.get(category, "others")
    category_md_path = f"routes/category/{category_slug}.md"

    # Markdown 内容模板
    md_content = f"""
## {site_url}

- **RSS URL**: [{rss_url}]({rss_url})
- **Description**: {rss_description}

---
"""

    # 更新主题分类的 Markdown 文件
    with open(category_md_path, "a") as category_md:
        category_md.write(md_content)

    print(f"Updated {category_md_path} with new RSS route for {category}.")


def main():
    site_url, rss_url, rss_description, category = extract_issue_input(issue_body)

    if not site_url or not rss_url or not rss_description or not category:
        print("必要的字段缺失，请确保所有信息填写完整。")
        return

    if not check_url_accessibility(site_url):
        print(f"警告：{site_url} 无法访问，但继续处理。")

    if not check_url_accessibility(rss_url):
        print(f"错误：{rss_url} 无法访问。")
        return

    if not rss_url.endswith("/"):
        rss_url += "/"

    domain = site_url.split(".")[-1]
    if domain not in ["com", "org", "net", "dev"]:
        print(f"错误：不支持的域名类型：{domain}")
        return

    key = generate_key_from_url(site_url)
    update_json_file(domain, key, rss_url)
    create_or_update_markdown(domain, category, site_url, rss_url, rss_description)
    print(f"成功更新 {domain}.json 和分类 Markdown 文档。")


if __name__ == "__main__":
    main()
