#!/usr/bin/env python3
"""
RSS 资讯抓取模块
"""
import feedparser
from datetime import datetime
from typing import List, Dict

# 完整的 RSS 源清单
RSS_FEEDS = [
    # AI 前沿与大模型
    ("arXiv AI", "http://export.arxiv.org/rss/cs.AI"),
    ("Hugging Face Papers", "https://huggingface.co/papers/rss"),
    ("OpenAI Blog", "https://openai.com/blog/rss.xml"),
    ("Anthropic", "https://www.anthropic.com/rss.xml"),
    ("MIT Tech Review AI", "https://www.technologyreview.com/topic/artificial-intelligence/feed"),
    
    # 生命科学与脑机接口
    ("Nature Machine Intelligence", "https://www.nature.com/natmachintell.rss"),
    ("Nature Neuroscience", "https://www.nature.com/neuro.rss"),
    ("IEEE Spectrum Robotics", "https://spectrum.ieee.org/feeds/feed.rss?topic=robotics"),
    ("bioRxiv Neuroscience", "https://connect.biorxiv.org/biorxiv_xml.php?subject=neuroscience"),
    ("Neuralink", "https://neuralink.com/blog/feed/"),
    
    # 市场趋势与社会影响
    ("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/feed/"),
    ("AI Impacts", "https://aiimpacts.org/feed/"),
]

def fetch_feeds(max_entries: int = 5) -> List[Dict]:
    """
    抓取所有 RSS 源
    """
    all_entries = []
    
    for feed_name, feed_url in RSS_FEEDS:
        print(f"📡 抓取：{feed_name}")
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:max_entries]:
                all_entries.append({
                    "source": feed_name,
                    "title": entry.title,
                    "summary": entry.get('summary', entry.get('description', '无摘要')),
                    "link": entry.link,
                    "published": entry.get('published', datetime.now().isoformat()),
                })
        except Exception as e:
            print(f"❌ {feed_name} 抓取失败：{e}")
    
    print(f"✅ 共抓取 {len(all_entries)} 条资讯\n")
    return all_entries

if __name__ == "__main__":
    entries = fetch_feeds()
    for e in entries[:3]:
        print(f"- {e['title']}")
