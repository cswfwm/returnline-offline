#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用 GitHub API 提交整个项目。空仓库先以 README 建立初始 commit，再以 Git Data API 批量提交全部文件。"""
import json, os, base64, sys, urllib.error, urllib.request

TOKEN = os.environ["GH_TOKEN"]
REPO = "cswfwm/returnline-offline"
PROJECT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GIT = "https://api.github.com/repos/" + REPO + "/git/"
CONTENTS = "https://api.github.com/repos/" + REPO + "/contents/"

SKIP_DIRS = {".git", ".aicode", "build", ".gradle", ".idea", ".cxx"}
SKIP_EXT = {".iml"}
SKIP_FILES = {"local.properties"}

def req(method, url, data=None):
    r = urllib.request.Request(url, method=method)
    r.add_header("Authorization", "Bearer " + TOKEN)
    r.add_header("Accept", "application/vnd.github+json")
    body = json.dumps(data).encode() if data is not None else None
    if body:
        r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, body) as resp:
            raw = resp.read()
            return resp.status, (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:
        raw = e.read() or b"{}"
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, {"message": raw.decode(errors="replace")}

def collect():
    files = []
    for root, dirs, names in os.walk(PROJECT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for n in names:
            if n in SKIP_FILES:
                continue
            if any(n.endswith(e) for e in SKIP_EXT):
                continue
            p = os.path.join(root, n)
            rel = os.path.relpath(p, PROJECT).replace(os.sep, "/")
            files.append((rel, p))
    return files

def is_binary(path):
    with open(path, "rb") as f:
        return b"\x00" in f.read(8000)

def init_repo():
    """若仓库为空，用 Contents API 写 README 建立初始 commit。返回默认分支 head sha。"""
    st, res = req("GET", GIT + "ref/heads/main")
    if st == 200 and "object" in res:
        return res["object"]["sha"]
    if st != 200 and st != 404:
        print("查 head 失败", st, res); sys.exit(1)
    # 空仓库：Contents API 上传 README
    st, res = req("PUT", CONTENTS + "README.md", {
        "message": "init: ProotShell container APK",
        "content": base64.b64encode(b"# ProotShell\nAndroid 5.1 armv7 extensible Linux container APK.\n").decode(),
    })
    if st not in (200, 201):
        print("init README 失败", st, res); sys.exit(1)
    st, res = req("GET", GIT + "ref/heads/main")
    return res["object"]["sha"]

def main():
    head = init_repo()
    print("head:", head[:8])

    # 取 base tree
    st, res = req("GET", GIT + "commits/" + head)
    base_tree = res["tree"]["sha"]

    files = collect()
    print(f"共 {len(files)} 个文件")
    entries = []
    for rel, p in files:
        if is_binary(p):
            with open(p, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            st, blob = req("POST", GIT + "blobs", {"content": b64, "encoding": "base64"})
        else:
            with open(p, "r", encoding="utf-8") as f:
                content = f.read()
            st, blob = req("POST", GIT + "blobs", {"content": content, "encoding": "utf-8"})
        if st != 201 or "sha" not in blob:
            print(f"blob 失败 {rel}: {st} {blob}"); return 1
        mode = "100755" if rel.endswith("gradlew") else "100644"
        entries.append({"path": rel, "mode": mode, "type": "blob", "sha": blob["sha"]})
        print(f"  + {rel}")

    st, tree = req("POST", GIT + "trees", {"base_tree": base_tree, "tree": entries})
    if st != 201:
        print("tree 失败", st, tree); return 1
    print("tree:", tree["sha"][:8])

    st, commit = req("POST", GIT + "commits", {
        "message": "ProotShell: Android 5.1 armv7 extensible Linux container APK (PRoot + Alpine + OpenAI agent)",
        "tree": tree["sha"],
        "parents": [head],
    })
    if st != 201:
        print("commit 失败", st, commit); return 1
    print("commit:", commit["sha"][:8])

    st, ref = req("PATCH", GIT + "refs/heads/main", {"sha": commit["sha"]})
    if st != 200:
        print("ref 失败", st, ref); return 1
    print("推送完成")
    return 0

if __name__ == "__main__":
    sys.exit(main())