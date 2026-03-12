#!/usr/bin/env python3
"""
AI 资讯选题系统 - 主程序
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent))

from fetcher import fetch_feeds
from evaluator import evaluate_entry
from publisher import publish_entry

def main():
    # 加载环境变量
    config_dir = Path(__file__).parent.parent / "config"
    load_dotenv(config_dir / ".env")
    
    # 读取配置
    # GitHub Actions 会自动提供 GITHUB_TOKEN 环境变量
    github_token = os.getenv("GITHUB_TOKEN")
    
    # 硬编码仓库名（不依赖环境变量）
    github_repo = "lalahoney11-pixel/ai-news-workspace"
    min_score = int(os.getenv("MIN_SCORE", "7"))
    max_entries = int(os.getenv("MAX_ENTRIES_PER_FEED", "5"))
    
    # API Keys
    api_keys = {
        "gemini": os.getenv("GEMINI_API_KEY"),
        "groq": os.getenv("GROQ_API_KEY"),
    }
    
    # GitHub Actions 会自动提供 GITHUB_TOKEN
    # 如果是本地运行没有 Token，给个警告但继续
    if not github_token:
        print("⚠️  警告：GITHUB_TOKEN 未设置，将无法发布 Issue")
        print("   GitHub Actions 会自动提供此变量")
        github_token = ""
    
    print("=" * 50)
    print("🦞 AI 资讯选题系统启动")
    print("=" * 50)
    print(f"📦 目标仓库：{github_repo}")
    print(f"⭐ 最低分数：{min_score}")
    print(f"📡 每个源抓取：{max_entries} 条")
    print()
    
    # 1. 抓取资讯
    entries = fetch_feeds(max_entries)
    
    # 2. AI 评估并发布
    published_count = 0
    for i, entry in enumerate(entries, 1):
        print(f"\n[{i}/{len(entries)}] 评估：{entry['title'][:50]}...")
        
        evaluation = evaluate_entry(entry, api_keys)
        if not evaluation:
            print("  ❌ 评估失败，跳过")
            continue
        
        score = evaluation.get('score', 0)
        print(f"  📊 评分：{score}/10")
        print(f"  🏷️  标签：{', '.join(evaluation.get('tags', []))}")
        print(f"  💡 理由：{evaluation.get('reason', '')}")
        
        # 3. 发布高分内容到 GitHub
        if score >= min_score:
            try:
                issue_url = publish_entry(github_repo, github_token, entry, evaluation)
                print(f"  ✅ 已发布：{issue_url}")
                published_count += 1
            except Exception as e:
                print(f"  ❌ 发布失败：{e}")
        else:
            print(f"  💤 分数低于阈值，跳过")
    
    # 总结
    print("\n" + "=" * 50)
    print(f"🎉 完成！共发布 {published_count}/{len(entries)} 条高分资讯")
    print(f"🔗 查看：https://github.com/{github_repo}/issues")
    print("=" * 50)

if __name__ == "__main__":
    main()
