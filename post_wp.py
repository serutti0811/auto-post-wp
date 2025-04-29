import os
import sys
import requests
import frontmatter   # pip install python-frontmatter

# ─────────────────────────────────────────────
#  環境変数から WordPress 認証情報を取得
# ─────────────────────────────────────────────
WP_USER    = os.getenv("WP_USER")          # 例: ai_writer
WP_APP_PW  = os.getenv("WP_APP_PW")        # 24 桁トークン
WP_SITE    = os.getenv("WP_SITE_URL", "https://gorogorostyle.com")  # ← 自サイトURL

if not (WP_USER and WP_APP_PW):
    raise SystemExit("WP_USER / WP_APP_PW が環境変数に設定されていません。")

AUTH = (WP_USER, WP_APP_PW)

# ─────────────────────────────────────────────
#  マークダウン + Front-Matter を WP へ投稿
# ─────────────────────────────────────────────
def post_markdown(md_path: str) -> None:
    post_obj = frontmatter.load(md_path)

    # Front-Matter が無い場合のフォールバック
    title   = post_obj.metadata.get("title",   "Auto Post")
    status  = post_obj.metadata.get("status",  "draft")   # publish に変えれば即公開
    tags    = post_obj.metadata.get("tags",    [])        # 例: [23, 45]
    date_gmt = post_obj.metadata.get("date_gmt")          # 予約投稿したいとき

    payload = {
        "title":   title,
        "content": post_obj.content,
        "status":  status,
        "tags":    tags,
    }
    if date_gmt:
        payload["date_gmt"] = date_gmt

    res = requests.post(
        f"{WP_SITE.rstrip('/')}/wp-json/wp/v2/posts",
        auth=AUTH,
        json=payload,
        timeout=30,
    )
    res.raise_for_status()
    data = res.json()
    print(f"✅  投稿成功: {data['id']} → {data['link']}")

# ─────────────────────────────────────────────
#  エントリポイント
# ─────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使い方: python post_wp.py <markdownファイル>")
        sys.exit(1)

    post_markdown(sys.argv[1])
