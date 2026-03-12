#!/usr/bin/env python3
"""
AI 评估模块 - 支持多个免费 API
"""
import json
import os
from typing import Dict, Optional

def evaluate_with_gemini(title: str, summary: str, api_key: str) -> Optional[Dict]:
    """使用 Google Gemini API 评估"""
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""你是一个资深科技媒体主编，专注 AI 前沿、生命科学、脑机接口、技术社会影响。
评估以下资讯的选题价值：

标题：{title}
摘要：{summary}

严格以 JSON 格式输出：
{{
  "score": 1-10 的整数，
  "tags": ["标签 1", "标签 2"],
  "reason": "20 字以内的理由"
}}

只输出 JSON，无其他文字。"""
        
        response = model.generate_content(prompt)
        text = response.text.strip()
        # 清理可能的 markdown 代码块标记
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        return json.loads(text.strip())
    except Exception as e:
        print(f"⚠️ Gemini 评估失败：{e}")
        return None

def evaluate_with_groq(title: str, summary: str, api_key: str) -> Optional[Dict]:
    """使用 Groq API 评估（速度快）"""
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        
        prompt = f"""你是一个资深科技媒体主编，专注 AI 前沿、生命科学、脑机接口、技术社会影响。
评估以下资讯的选题价值：

标题：{title}
摘要：{summary}

严格以 JSON 格式输出：
{{
  "score": 1-10 的整数，
  "tags": ["标签 1", "标签 2"],
  "reason": "20 字以内的理由"
}}

只输出 JSON，无其他文字。"""
        
        response = client.chat.completions.create(
            model="llama-3.2-90b-vision-preview",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=200
        )
        text = response.choices[0].message.content.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        return json.loads(text.strip())
    except Exception as e:
        print(f"⚠️ Groq 评估失败：{e}")
        return None

def evaluate_entry(entry: Dict, api_keys: Dict) -> Optional[Dict]:
    """
    尝试多个 API，返回第一个成功的结果
    """
    title = entry['title']
    summary = entry['summary']
    
    # 尝试 Gemini
    if api_keys.get('gemini'):
        print(f"  🤖 使用 Gemini 评估...")
        result = evaluate_with_gemini(title, summary, api_keys['gemini'])
        if result:
            return result
    
    # 尝试 Groq
    if api_keys.get('groq'):
        print(f"  🤖 使用 Groq 评估...")
        result = evaluate_with_groq(title, summary, api_keys['groq'])
        if result:
            return result
    
    # 降级方案：简单关键词打分
    print(f"  ⚡ 使用关键词快速打分...")
    keywords = ['AI', 'neural', 'brain', 'robot', 'model', 'learning', 'interface', 'AGI']
    score = 5 + sum(1 for kw in keywords if kw.lower() in (title + summary).lower())
    return {
        "score": min(score, 10),
        "tags": ["AI 前沿"],
        "reason": "关键词匹配度较高"
    }

if __name__ == "__main__":
    # 测试
    test_entry = {
        "title": "New AI Model Achieves Human-Level Performance",
        "summary": "Researchers announce breakthrough in artificial intelligence..."
    }
    result = evaluate_entry(test_entry, {})
    print(result)
