import os
import pathlib, random
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tails = ["ね。", "よ。", "だ。", "！"]

for draft in pathlib.Path(".").glob("draft_*.md"):
    refined = draft.name.replace("draft_", "refined_", 1)
    prompt  = f"以下の記事を自然な言い回しにパラフレーズしてください。\n\n{draft.read_text(encoding='utf-8')}"
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.85,
            max_tokens=1400,
            messages=[{"role":"user", "content": prompt}]
        )
        body = resp.choices[0].message.content.strip()
    except Exception as e:
        print("❌ refine error:", e)
        continue

    body = body.rstrip("。") + random.choice(tails) + "\n"
    pathlib.Path(refined).write_text(body, encoding="utf-8")
    print(f"✅ refined saved: {refined}")
