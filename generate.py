import os
import datetime
import random
import pathlib
import json
import slugify
import openai

# ───────────────────────────────
#  1) 記事ネタ候補（必要に応じて動的取得に差し替え）
# ───────────────────────────────
TOPICS = [
    "副業 ブログ",
    "AI ライティング",
    "プログラミングスクール",
    "デジタルノマド",
    "ウェルビーイング 習慣"
]

# ───────────────────────────────
#  2) OpenAI APIキー
# ───────────────────────────────
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise SystemExit("OPENAI_API_KEY が環境変数に設定されていません。")

# ───────────────────────────────
#  3) プロンプト雛形を読み込む
# ───────────────────────────────
PROMPT_PATH = pathlib.Path("prompt.txt")
if not PROMPT_PATH.exists():
    raise SystemExit("prompt.txt が見つかりません。")

prompt_template = PROMPT_PATH.read_text(encoding="utf-8")

# ───────────────────────────────
#  4) Draft を生成してファイル保存
# ───────────────────────────────
def main() -> None:
    topic = random.choice(TOPICS)
    prompt = prompt_template.format(topic=topic)

    # OpenAI コールを try–except で包み、エラー内容を必ず表示
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            temperature=0.7,
            max_tokens=1200,
            messages=[{"role": "user", "content": prompt}]
        )
    except Exception as e:
        print("❌ OpenAI API error:", e)
        raise  # exit code 1 → GitHub Actions を失敗扱いに

    content = resp.choices[0].message.content.strip()

    slug = slugify.slugify(topic) + "-" + datetime.date.today().isoformat()
    draft_path = pathlib.Path(f"draft_{slug}.md")

    # Front-Matter（必要最低限）
    fm = {
        "title":  topic,
        "status": "draft"          # 自動公開したい場合は "publish"
    }
    markdown = "---\n" + json.dumps(fm, ensure_ascii=False, indent=2) + "\n---\n\n" + content

    draft_path.write_text(markdown, encoding="utf-8")
    print(f"✅ Draft saved: {draft_path}")

# ───────────────────────────────
if __name__ == "__main__":
    main()
