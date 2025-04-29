import pathlib
import random
import shutil

# draft_*.md を探す
for draft in pathlib.Path(".").glob("draft_*.md"):
    # 出力ファイル名: refined_YYYY-MM-DD.md
    refined = draft.name.replace("draft_", "refined_", 1)

    # 本文を読み込む
    text = draft.read_text(encoding="utf-8")

    # 超簡易「人間味」…語尾にゆらぎを 1 個だけ入れる例
    tails = ["ね。", "よ。", "だ。", "！"]
    text = text.rstrip("。") + random.choice(tails) + "\n"

    # コピー & 上書き
    pathlib.Path(refined).write_text(text, encoding="utf-8")
    print(f"✅  refined saved: {refined}")
