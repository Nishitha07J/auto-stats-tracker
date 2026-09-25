# 📊 Coding Stats Auto-Updater

Automatically update your GitHub profile README with your live Codeforces and LeetCode stats — updated daily via GitHub Actions, zero servers, completely free.

## 🚀 Setup (takes ~2 minutes)

1. Click **"Use this template"** above to create your own copy of this repo.
   - ⚠️ If you want this on your GitHub *profile*, name your new repo exactly the same as your GitHub username, and make it public.
2. Open `config.json` and fill in your usernames:
```json
   {
     "codeforces_username": "your_handle",
     "leetcode_username": "your_handle"
   }
```
3. Commit the change.
4. Go to the **Actions** tab of your new repo and click **"Run workflow"** to trigger it manually the first time (after that, it runs automatically every midnight UTC).
5. Check your `README.md` — your stats table should now appear below!

## ⚙️ How it works

- A Python script fetches your stats from the Codeforces API and LeetCode's GraphQL endpoint
- A GitHub Actions workflow runs the script on a daily cron schedule
- The script updates the content between `<!--STATS:START-->
No usernames configured in config.json yet.
<!--STATS:END-->` in your README and auto-commits the change

## 🛠️ Customize

- Leave a username blank in `config.json` to skip that platform
- Want to change the update time? Edit the `cron` value in `.github/workflows/update.yml` (times are in UTC)

## 📄 License

MIT — free to use and modify.

---

<!--STATS:START-->
<!--STATS:END-->
