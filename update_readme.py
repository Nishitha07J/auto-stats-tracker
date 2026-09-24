import json
import requests

# ---------- Load config ----------
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

cf_username = config.get("codeforces_username", "").strip()
lc_username = config.get("leetcode_username", "").strip()


# ---------- Codeforces ----------
def get_codeforces_stats(username):
    try:
        response = requests.get(f"https://codeforces.com/api/user.info?handles={username}", timeout=10)
        data = response.json()
        if data["status"] == "OK":
            user = data["result"][0]
            return {
                "rating": user.get("rating", "Unrated"),
                "rank": user.get("rank", "Unranked"),
                "max_rating": user.get("maxRating", "N/A"),
            }
    except Exception as e:
        print(f"Codeforces fetch failed: {e}")
    return None


# ---------- LeetCode ----------
def get_leetcode_stats(username):
    url = "https://leetcode.com/graphql"
    query = """
    query getUserProfile($username: String!) {
      matchedUser(username: $username) {
        username
        submitStats: submitStatsGlobal {
          acSubmissionNum { difficulty count }
        }
        profile { ranking }
      }
    }
    """
    try:
        response = requests.post(
            url,
            json={"query": query, "variables": {"username": username}},
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10,
        )
        data = response.json()
        matched_user = data.get("data", {}).get("matchedUser")
        if not matched_user:
            return None
        ranking = matched_user["profile"]["ranking"]
        solved = {item["difficulty"]: item["count"] for item in matched_user["submitStats"]["acSubmissionNum"]}
        return {
            "ranking": ranking,
            "total_solved": solved.get("All", 0),
            "easy": solved.get("Easy", 0),
            "medium": solved.get("Medium", 0),
            "hard": solved.get("Hard", 0),
        }
    except Exception as e:
        print(f"LeetCode fetch failed: {e}")
    return None


# ---------- Build markdown ----------
stats_md = ""

if cf_username:
    cf_stats = get_codeforces_stats(cf_username)
    stats_md += "### Codeforces\n"
    if cf_stats:
        stats_md += f"""| Metric | Value |
|---|---|
| Handle | {cf_username} |
| Current Rating | {cf_stats['rating']} |
| Rank | {cf_stats['rank']} |
| Max Rating | {cf_stats['max_rating']} |
"""
    else:
        stats_md += "Could not fetch Codeforces stats.\n"

if lc_username:
    lc_stats = get_leetcode_stats(lc_username)
    stats_md += "\n### LeetCode\n"
    if lc_stats:
        stats_md += f"""| Metric | Value |
|---|---|
| Handle | {lc_username} |
| Ranking | {lc_stats['ranking']} |
| Total Solved | {lc_stats['total_solved']} |
| Easy | {lc_stats['easy']} |
| Medium | {lc_stats['medium']} |
| Hard | {lc_stats['hard']} |
"""
    else:
        stats_md += "Could not fetch LeetCode stats.\n"

if not stats_md:
    stats_md = "No usernames configured in config.json yet."


# ---------- Update README ----------
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "<!--STATS:START-->"
end_marker = "<!--STATS:END-->"

start_idx = content.find(start_marker) + len(start_marker)
end_idx = content.find(end_marker)

new_content = content[:start_idx] + "\n" + stats_md + "\n" + content[end_idx:]

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_content)

print("README updated.")
