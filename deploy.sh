#!/bin/bash
# 快速部署脚本

echo "🦞 AI 资讯选题系统 - 部署脚本"
echo "================================"

# 检查是否在正确的目录
if [ ! -f "src/main.py" ]; then
    echo "❌ 请在 ai-news-agent 目录下运行此脚本"
    exit 1
fi

# 创建 GitHub 仓库（需要 gh CLI）
if command -v gh &> /dev/null; then
    echo "📦 创建 GitHub 仓库..."
    gh repo create ai-news-workspace --public --source=. --remote=origin --push
else
    echo "⚠️  未检测到 GitHub CLI，请手动操作："
    echo "1. 在 GitHub 创建新仓库：ai-news-workspace"
    echo "2. 然后运行："
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    echo "   git remote add origin https://github.com/lalahoney11-pixel/ai-news-workspace.git"
    echo "   git push -u origin main"
fi

echo ""
echo "✅ 部署完成！"
echo ""
echo "📋 下一步："
echo "1. 在 GitHub 仓库 Settings → Secrets and variables → Actions 添加 Secrets:"
echo "   - GITHUB_TOKEN: 你的 GitHub Token"
echo "   - GITHUB_REPO: lalahoney11-pixel/ai-news-workspace"
echo "   - GEMINI_API_KEY: (可选) Google AI Studio Key"
echo "   - GROQ_API_KEY: (可选) Groq Key"
echo ""
echo "2. 获取 API Keys:"
echo "   - Gemini: https://aistudio.google.com/app/apikey"
echo "   - Groq: https://console.groq.com/keys"
echo ""
echo "3. 在 Actions 页面手动触发一次 'Daily AI News Fetch'"
echo ""
echo "🔗 仓库地址：https://github.com/lalahoney11-pixel/ai-news-workspace"
