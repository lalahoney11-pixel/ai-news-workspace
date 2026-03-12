# 🦞 AI 资讯选题系统

全自动 AI 前沿资讯抓取、评估、发布系统

## 功能特点

- 📡 **多源聚合** - arXiv、Nature、IEEE、TechCrunch 等 12+ 顶级信源
- 🤖 **AI 智能评估** - 支持 Gemini、Groq 多个免费 API
- ⭐ **自动打分** - 1-10 分评分系统，只保留 7 分以上高质量内容
- 📦 **GitHub 看板** - 自动创建 Issue，可用 Projects 管理选题
- ⏰ **定时运行** - GitHub Actions 每天自动执行

## 信源清单

### AI 前沿与大模型
- arXiv AI (cs.AI)
- Hugging Face Papers
- OpenAI Blog
- Anthropic
- MIT Technology Review AI

### 生命科学与脑机接口
- Nature Machine Intelligence
- Nature Neuroscience
- IEEE Spectrum Robotics
- bioRxiv Neuroscience
- Neuralink

### 市场趋势与社会影响
- TechCrunch AI
- AI Impacts

## 快速开始

### 1. 克隆到你的仓库

```bash
# 在你的 GitHub 上创建新仓库 ai-news-workspace
# 然后克隆并推送代码
git clone https://github.com/lalahoney11-pixel/ai-news-workspace.git
cd ai-news-workspace
# 把本项目的文件复制进去
git add .
git commit -m "Initial commit"
git push
```

### 2. 配置 Secrets

在 GitHub 仓库的 **Settings → Secrets and variables → Actions** 中添加：

| 名称 | 值 |
|------|-----|
| `GITHUB_TOKEN` | 你的 GitHub Personal Access Token (repo 权限) |
| `GITHUB_REPO` | `lalahoney11-pixel/ai-news-workspace` |
| `GEMINI_API_KEY` | (可选) Google AI Studio API Key |
| `GROQ_API_KEY` | (可选) Groq API Key |

### 3. 获取 API Keys

**Google Gemini (免费额度):**
1. 访问 https://aistudio.google.com/app/apikey
2. 创建 API Key
3. 复制到 Secrets

**Groq (目前免费):**
1. 访问 https://console.groq.com/keys
2. 创建 API Key
3. 复制到 Secrets

### 4. 运行

**手动触发:**
```bash
# 本地测试
pip install -r requirements.txt
cp config/.env.example config/.env
# 编辑 config/.env 填入你的 keys
python src/main.py
```

**自动运行:**
- 每天北京时间 8 点自动执行
- 或在 GitHub Actions 页面手动触发

## 输出效果

每条高分资讯会自动创建为 GitHub Issue：

```
Title: [8 分] New Breakthrough in Brain-Computer Interface

Body:
### 💡 AI 推荐理由
**突破机器人手部精细控制瓶颈** (AI 评分：8/10)

### 🏷️ 标签
`脑机接口` `前沿研究`

### 📝 资讯摘要
...

### 🔗 原文链接
[点击阅读原文](...)
```

## 使用 GitHub Projects

1. 在仓库中创建 **Projects** (Beta)
2. 选择 **Board** 视图
3. 添加列：`📥 待处理` `✍️ 写作中` `✅ 已发布`
4. 把 Issue 拖拽到对应列

## 扩展

### 添加新信源
编辑 `src/fetcher.py` 中的 `RSS_FEEDS` 列表

### 调整评分阈值
在 Secrets 中添加变量 `MIN_SCORE` (默认 7)

### 自定义评估 Prompt
编辑 `src/evaluator.py` 中的 Prompt 内容

## 技术栈

- Python 3.11+
- feedparser (RSS 解析)
- google-generativeai (Gemini API)
- groq (Groq API)
- GitHub Actions (自动化)

## License

MIT

---
🦞 Made with love by 龙虾
