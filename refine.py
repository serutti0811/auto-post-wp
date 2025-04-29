import os
import sys
import requests
import frontmatter   # pip install python-frontmatter

# ───────────────────────────────
#  WordPress 認証情報
# ───────────────────────────────
WP_USER   = os.getenv("WP_USER")          # 例: ai_writer
WP_APP_PW = os.getenv("WP_APP_PW")        # 24 桁トークン
WP_SITE   = os.getenv("WP_SITE_URL", "https://gorogorostyle.com")

if not (WP_USER and WP_APP_PW):
    raise SystemExit("WP_USER / WP_APP_PW が環境変数にありません。")

AUTH = (WP_USER, WP_APP_PW)

# ───────────────────────────────
#  markdown + Front Matter を投稿
# ───────────────────────────────
def post_markdown(md_path: str) -> None:
    post = frontmatter.load(md_path)

    title   = post.metadata.get("title",   "Auto Post")
    status  = post.metadata.get("status",  "draft")  # publish に変更可
    tags    = post.metadata.get("tags",    [])
    date_gmt = post.metadata.get("date_gmt")         # 予約投稿用

    payload = {
        "title":   title,
        "content": post.content,
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
    print(f"✅ 投稿成功: ID={data['id']} → {data['link']}")

# ───────────────────────────────
#  エントリポイント
# ───────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使い方: python post_wp.py <markdown_file>")
        sys.exit(1)

    post_markdown(sys.argv[1])
