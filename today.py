import os
import datetime
import requests

GITHUB_USERNAME = "rahul-1909"
HEADERS = {"Authorization": f"Bearer {os.environ.get('GH_TOKEN', os.environ.get('GITHUB_TOKEN', ''))}"}

GRAPHQL_QUERY = """
query($username: String!) {
  user(login: $username) {
    name
    login
    createdAt
    followers { totalCount }
    repositories(first: 100, ownerAffiliations: OWNER, orderBy: {field: PUSHED_AT, direction: DESC}) {
      totalCount
      nodes {
        stargazerCount
        forkCount
      }
    }
    contributionsCollection {
      totalCommitContributions
      restrictedContributionsCount
    }
  }
}
"""

def fetch_stats():
    url = "https://api.github.com/graphql"
    response = requests.post(url, json={"query": GRAPHQL_QUERY, "variables": {"username": GITHUB_USERNAME}}, headers=HEADERS)
    
    if response.status_code != 200 or "data" not in response.json() or response.json()["data"]["user"] is None:
        return {
            "name": "Rahul Teja Nalla",
            "username": GITHUB_USERNAME,
            "repos": 10,
            "stars": 5,
            "followers": 5,
            "commits": "100+",
            "uptime": "Active"
        }
    
    data = response.json()["data"]["user"]
    created_at = datetime.datetime.fromisoformat(data["createdAt"].replace("Z", "+00:00"))
    uptime_days = (datetime.datetime.now(datetime.timezone.utc) - created_at).days
    years = uptime_days // 365
    days = uptime_days % 365

    repos = data["repositories"]["totalCount"]
    stars = sum(node["stargazerCount"] for node in data["repositories"]["nodes"])
    followers = data["followers"]["totalCount"]
    commits = data["contributionsCollection"]["totalCommitContributions"] + data["contributionsCollection"]["restrictedContributionsCount"]

    return {
        "name": data["name"] or "Rahul Teja Nalla",
        "username": data["login"],
        "repos": repos,
        "stars": stars,
        "followers": followers,
        "commits": f"{commits:,}",
        "uptime": f"{years} yrs, {days} days"
    }

def generate_svg(stats, dark_mode=True):
    bg_color = "#0d1117" if dark_mode else "#ffffff"
    border_color = "#30363d" if dark_mode else "#d0d7de"
    text_primary = "#58a6ff" if dark_mode else "#0969da"
    text_secondary = "#c9d1d9" if dark_mode else "#24292f"
    text_label = "#7ee787" if dark_mode else "#1a7f37"
    text_accent = "#ffa657" if dark_mode else "#bc4c00"
    text_purple = "#d2a8ff" if dark_mode else "#8250df"
    
    ascii_art = [
        "      ___          ___      ",
        "     /\\  \\        /\\  \\     ",
        "    /::\\  \\      /::\\  \\    ",
        "   /:/\\:\\  \\    /:/\\:\\  \\   ",
        "  /::\\~\\:\\  \\  /::\\~\\:\\  \\  ",
        " /:/\\:\\ \\:\\__\\/:/\\:\\ \\:\\__\\ ",
        " \\/_|::\\/:/  /\\/_|::\\/:/  / ",
        "    |:|::/  /    |:|::/  /  ",
        "    |:|\\/__/     |:|\\/__/   ",
        "    |:|  |       |:|  |     ",
        "     \\|__|        \\|__|     "
    ]

    ascii_lines_svg = "\n".join([
        f'<tspan x="30" dy="18">{line}</tspan>' for line in ascii_art
    ])

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="750" height="320" viewBox="0 0 750 320">
  <style>
    .terminal {{ font-family: 'Fira Code', 'Courier New', monospace; font-size: 13px; fill: {text_secondary}; }}
    .ascii {{ font-family: 'Fira Code', monospace; font-size: 12px; font-weight: bold; fill: {text_primary}; }}
    .title {{ font-size: 14px; font-weight: bold; fill: {text_primary}; }}
    .label {{ font-weight: bold; fill: {text_label}; }}
    .accent {{ fill: {text_accent}; }}
    .purple {{ fill: {text_purple}; }}
    .palette {{ font-size: 14px; }}
  </style>
  <rect width="100%" height="100%" rx="10" fill="{bg_color}" stroke="{border_color}" stroke-width="1.5"/>
  
  <!-- ASCII Art Section -->
  <text class="ascii" y="55">
    {ascii_lines_svg}
  </text>
  
  <!-- Neofetch Info Section -->
  <g transform="translate(290, 45)">
    <text class="terminal">
      <tspan class="title" x="0" y="0">{stats['username']}@github</tspan>
      <tspan x="0" y="16" fill="{border_color}">------------------------------------</tspan>
      
      <tspan class="label" x="0" y="40">OS:</tspan><tspan x="100" y="40">Ubuntu 24.04 LTS / macOS</tspan>
      <tspan class="label" x="0" y="62">Host:</tspan><tspan x="100" y="62">Full-Stack Developer</tspan>
      <tspan class="label" x="0" y="84">Kernel:</tspan><tspan x="100" y="84">Python, TypeScript, SQL</tspan>
      <tspan class="label" x="0" y="106">Uptime:</tspan><tspan x="100" y="106">{stats['uptime']}</tspan>
      <tspan class="label" x="0" y="128">Packages:</tspan><tspan x="100" y="128">{stats['repos']} (repos)</tspan>
      <tspan class="label" x="0" y="150">Shell:</tspan><tspan x="100" y="150">zsh 5.9 (x86_64)</tspan>
      <tspan class="label" x="0" y="172">Stars:</tspan><tspan x="100" y="172" class="accent">{stats['stars']} ★</tspan>
      <tspan class="label" x="0" y="194">Commits:</tspan><tspan x="100" y="194" class="purple">{stats['commits']}</tspan>
      <tspan class="label" x="0" y="216">Followers:</tspan><tspan x="100" y="216">{stats['followers']}</tspan>
      
      <!-- Color Palette -->
      <tspan class="palette" x="0" y="248">
        <tspan fill="#ff5f56">● </tspan>
        <tspan fill="#ffbd2e">● </tspan>
        <tspan fill="#27c93f">● </tspan>
        <tspan fill="#007acc">● </tspan>
        <tspan fill="#d2a8ff">● </tspan>
        <tspan fill="#00bcd4">● </tspan>
        <tspan fill="#ffffff">● </tspan>
      </tspan>
    </text>
  </g>
</svg>"""

if __name__ == "__main__":
    stats = fetch_stats()
    
    with open("dark_mode.svg", "w", encoding="utf-8") as f:
        f.write(generate_svg(stats, dark_mode=True))
        
    with open("light_mode.svg", "w", encoding="utf-8") as f:
        f.write(generate_svg(stats, dark_mode=False))
