import pathlib
import random

# draft_*.md を探して refined_*.md にコピー＋語尾を1文字ゆらす
for draft in pathlib.Path(".").glob("draft_*.md"):
    refined = draft.name.replace("draft_", "refined_", 1)

    body = draft.read_text(encoding="utf-8").rstrip()

    tails = ["ね。", "よ。", "だ。", "！"]
    body = body.rstrip("。") + random.choice(tails) + "\n"

    pathlib.Path(refined).write_text(body, encoding="utf-8")
    print(f"✅ refined saved: {refined}")
