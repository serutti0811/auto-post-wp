import os, datetime, random, pathlib, json
import slugify
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
if client.api_key is None:
    raise SystemExit("OPENAI_API_KEY が環境変数にありません。")

TOPICS = [
    "副業 ブログ", "AI ライティング", "プログラミングスクール",
    "デジタルノマド", "ウェルビーイング 習慣"
]

PROMPT_PATH = pathlib.Path("prompt.txt")
prompt_template = PROMPT_PATH.read_text(encoding="utf-8")

def main():
    topic  = random.choice(TOPICS)
    prompt = prompt_template.format(topic=topic)

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.7,
            max_tokens=1200,
            messages=[{"role":"user","content":prompt}]
        )
    except Exception as e:
        print("❌ OpenAI error:", e)
        raise

    content = resp.choices[0].message.content.strip()
    slug = slugify.slugify(topic) + "-" + datetime.date.today().isoformat()

    fm = {"title": topic, "status": "draft"}
    md = f"---\n{json.dumps(fm, ensure_ascii=False, indent=2)}\n---\n\n{content}"

    path = pathlib.Path(f"draft_{slug}.md")
    path.write_text(md, encoding="utf-8")
    print(f"✅ Draft saved: {path}")

if __name__ == "__main__":
    main()
