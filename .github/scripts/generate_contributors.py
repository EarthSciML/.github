#!/usr/bin/env python3
import requests
import os
import math
import base64
from io import BytesIO
from PIL import Image

ORG = os.environ["GITHUB_ORG"]
TOKEN = os.environ["GITHUB_TOKEN"]

print(f"Fetching repos for organization: {ORG}")

repos = []
page = 1
while True:
    r = requests.get(
        f"https://api.github.com/orgs/{ORG}/repos",
        params={"per_page": 100, "page": page},
        headers={"Authorization": f"token {TOKEN}"}
    )
    data = r.json()
    if not data or r.status_code != 200:
        break
    repos.extend(data)
    page += 1

print(f"Found {len(repos)} repositories.")

avatars = {}
for repo in repos:
    repo_name = repo["name"]
    print(f"Fetching contributors for: {repo_name}")
    page_c = 1
    while True:
        rc = requests.get(
            f"https://api.github.com/repos/{ORG}/{repo_name}/contributors",
            params={"per_page": 100, "page": page_c},
            headers={"Authorization": f"token {TOKEN}"}
        )
        contributors = rc.json()
        if not contributors or rc.status_code != 200:
            break
        for c in contributors:
            avatars[c["login"]] = c["avatar_url"]
        page_c += 1

print(f"Total unique contributors: {len(avatars)}")

# SVG layout settings
size = 64
cols = 10
rows = math.ceil(len(avatars) / cols)

svg_parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'xmlns:xlink="http://www.w3.org/1999/xlink" '
    f'width="{cols*size}" height="{rows*size}">'
]

for idx, (login, url) in enumerate(sorted(avatars.items())):
    img = Image.open(BytesIO(requests.get(url).content)).resize((size, size))
    buf = BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    x = (idx % cols) * size
    y = (idx // cols) * size
    profile_url = f"https://github.com/{login}"
    svg_parts.append(
        f'<a xlink:href="{profile_url}" target="_blank">'
        f'<image x="{x}" y="{y}" width="{size}" height="{size}" '
        f'xlink:href="data:image/png;base64,{b64}" />'
        f'</a>'
    )

svg_parts.append("</svg>")

with open("contributors.svg", "w") as f:
    f.write("\n".join(svg_parts))

print("Saved contributors.svg")