#!/usr/bin/env python3
"""
GitHub 发布模块 - 自动创建 Issue
"""
import requests
from typing import Dict, List

def create_github_issue(repo: str, token: str, title: str, body: str, labels: List[str]) -> str:
    """
    创建 GitHub Issue
    返回 Issue URL
    """
    url = f"https://api.github.com/repos/{repo}/issues"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "title": title,
        "body": body,
        "labels": labels
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        return response.json()['html_url']
    else:
        raise Exception(f"GitHub API 错误：{response.status_code} - {response.text}")

def publish_entry(repo: str, token: str, entry: Dict, evaluation: Dict) -> str:
    """
    将评估后的资讯发布为 GitHub Issue
    """
    title = f"[{evaluation['score']}分] {entry['title'][:80]}"
    
    body = f"""### 💡 AI 推荐理由
**{evaluation['reason']}** (AI 评分：{evaluation['score']}/10)

---

### 🏷️ 标签
{', '.join([f"`{tag}`" for tag in evaluation['tags']])}

---

### 📝 资讯摘要
{entry['summary'][:500]}{'...' if len(entry['summary']) > 500 else ''}

---

### 🔗 原文链接
[点击阅读原文]({entry['link']})

---

### 📰 来源
{entry['source']} | {entry['published']}

---
*本 Issue 由 AI 选题系统自动抓取并生成*
"""
    
    # 标签加上 emoji 前缀
    github_labels = [f"🤖 {tag}" for tag in evaluation['tags']]
    github_labels.append(f"⭐ {evaluation['score']}分")
    
    return create_github_issue(repo, token, title, body, github_labels)

if __name__ == "__main__":
    print("Publisher module loaded")
