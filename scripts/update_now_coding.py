"""배너의 'NOW CODING' 문구를 최근에 push한 공개 레포로 갱신한다.

- 포크와 프로필 레포(Astrum93/Astrum93) 자신은 제외
- 태그 중 가장 높은 버전(vX.Y.Z)이 있으면 붙인다 (예: "music_is_life v2.1.1")
- /users/{user}/repos 는 공개 레포만 돌려주므로 비공개 레포 이름은 노출되지 않는다
- 결과를 scripts/src/now_coding.txt 에 쓰고, 바뀌었는지 종료 메시지로 알린다

사용법: python3 scripts/update_now_coding.py  (저장소 루트에서 실행, GITHUB_TOKEN 있으면 사용)
"""
import json
import os
import re
import urllib.request

USER = "Astrum93"
OUT = "scripts/src/now_coding.txt"
API = "https://api.github.com"


def get(path):
    req = urllib.request.Request(API + path, headers={"Accept": "application/vnd.github+json",
                                                      "User-Agent": "profile-now-coding"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def latest_version(repo):
    best = None
    for t in get(f"/repos/{USER}/{repo}/tags?per_page=100"):
        m = re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)", t["name"])
        if m:
            key = tuple(int(x) for x in m.groups())
            if best is None or key > best[0]:
                best = (key, t["name"])
    return best[1] if best else None


def main():
    repos = get(f"/users/{USER}/repos?sort=pushed&direction=desc&per_page=20&type=owner")
    repo = next(r for r in repos if not r["fork"] and r["name"].lower() != USER.lower())
    version = latest_version(repo["name"])
    text = f'{repo["name"]} {version}' if version else repo["name"]
    old = open(OUT, encoding="utf-8").read().strip() if os.path.exists(OUT) else ""
    if text != old:
        with open(OUT, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        print(f"changed: {old!r} -> {text!r}")
    else:
        print(f"unchanged: {text!r}")


if __name__ == "__main__":
    main()
