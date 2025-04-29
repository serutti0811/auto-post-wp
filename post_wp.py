import os
import sys
import requests
import frontmatter

# ───────────────────────────────
#  WordPress 認証情報（Secrets から渡る）
# ───────────────────────────────
WP_USER   = os.getenv("WP_USER")
WP_APP_PW = os.getenv("WP_APP_PW")
WP_SITE   = os.getenv("WP_SITE_URL", "https://gorogorostyle.com")

if not (WP_USER and WP_APP_PW):
    raise SystemExit("WP_USER / WP_APP_PW が環境変数に設定されていません。")

AUTH = (WP_USER, WP_APP_PW)

# ───────────────────────────────
#  マークダウン + Front-Matter を投稿
# ───────────────────────────────
def post_markdown(md_path: str) -> None:
    post = frontmatter.load(md_path)

    payload = {
        "title":   post.metadata.get("title", "Auto Post"),
        "content": post.content,
        "status":  post.metadata.get("status", "draft"),  # publish に変えれば即公開
        "tags":    post.metadata.get("tags", []),
    }

    res = requests.post(
        f"{WP_SITE.rstrip('/')}/wp-json/wp/v2/posts",
        auth=AUTH,
        json=payload,
        timeout=30,
    )

    # ── 失敗時の本文を必ず表示 ──
    if res.status_code >= 400:
        print("❌ WP ERROR BODY:", res.status_code, res.text)
        res.raise_for_status()      # ここで exit code 1 になる

    data = res.json()
    print(f"✅ 投稿成功: {data['id']} → {data['link']}")

# ───────────────────────────────
#  エントリポイント
# ───────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("使い方: python post_wp.py <markdownファイル>")
    post_markdown(sys.argv[1])
