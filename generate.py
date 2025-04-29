import os, datetime, random, slugify, openai, json, pathlib

# ────────────────────────────
#  1. 生成に使うキーワードを用意
# ────────────────────────────
TOPICS = [
    "副業 ブログ",
    "AI ライティング",
    "プログラミングスクール",
    "デジタルノマド",
    "ウェルビーイング 習慣"
]

# RSS や GoogleTrends から自動取得したい場合は
# ここでリストを差し替えるだけで OK

# ────────────────────────────
#  2. OpenAI API KEY を読む
# ────────────────────────────
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise SystemExit("OPENAI_API_KEY が環境変数にありません。")

# ────────────────────────────
#  3. プロンプト雛形を読む
# ────────────────────────────
template_path = pathlib.Path("prompt.txt")
if not template_path.exists():
    raise SystemExit("prompt.txt が見つかりません。")

prompt_template = template_path
