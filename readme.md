# 🕷️ Selenium Website Change Tracker — Cheat Sheet

## 🎯 Goal
Track changes on a website (like TanitJobs):
- Scrape job listings
- Detect new / removed items
- Export to CSV / JSON
- Prepare for notifications (email / Telegram)
- Work **even with Cloudflare protection**

---

## 🧠 Core Concepts

### What is Selenium?
Selenium automates a **real browser** (Chrome, Firefox).
Unlike `requests`, it:
- Executes JavaScript
- Loads dynamic content
- Can bypass basic anti-bot systems

---

### What does *Headless* mean?
- **Headless = browser runs invisibly**
- Faster, but **more likely blocked**
- ❌ Avoid headless when Cloudflare is present
- ✅ Use visible browser + saved profile

---

## 🛡️ Cloudflare & CAPTCHA

If you see:
> *Verifying you are human*

It means:
- Site is protected by Cloudflare
- Requests-only scraping will fail

### ✅ Solution: Chrome Profile Reuse
1. Selenium opens Chrome **once**
2. You solve CAPTCHA manually
3. Session is saved
4. Future runs bypass CAPTCHA automatically

---

## ⚙️ Selenium Setup (Safe Mode)

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument(r"--user-data-dir=C:/Users/YOURNAME/selenium-profile")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
```

📌 First run = solve CAPTCHA  
📌 Later runs = fully automated  

---

## 🔍 Waiting for Elements (IMPORTANT)

Never scrape immediately.

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

wait = WebDriverWait(driver, 15)
jobs = wait.until(
    EC.presence_of_all_elements_located(
        (By.XPATH, '//article[contains(@class,"listing-item")]')
    )
)
```

---

## 🧩 Scraping Structure

HTML snippet:
```html
<article class="listing-item">
  <a class="link">Job title</a>
</article>
```

Scraping:
```python
title = job.find_element(By.XPATH, './/a[@class="link"]').text
link = job.find_element(By.XPATH, './/a[@class="link"]').get_attribute('href')
```

---

## 💾 Exporting Data

### CSV
```python
df.to_csv("jobs.csv", index=False)
```

### JSON
```python
df.to_json("jobs.json", orient="records")
```

---

## 🔄 Detecting Changes (Magic Part ✨)

```python
merged = today.merge(
    previous,
    on="Title",
    how="outer",
    indicator=True
)

new = merged[merged["_merge"] == "left_only"]
removed = merged[merged["_merge"] == "right_only"]
```

Use this to:
- Notify yourself
- Track history
- Update Google Sheets

---

## ⏱️ How Changes Are Detected

❌ Website does NOT notify you  
✅ You **poll** it periodically

Flow:
```
Run script every X hours
↓
Scrape current state
↓
Compare with last snapshot
↓
If different → trigger alert
```

---

## 📅 Automation (Later Step)

- Windows → Task Scheduler
- Linux/Mac → cron job

Example:
```
Every 6 hours
```

---

## 🔔 Notifications (Next Upgrade)

Possible channels:
- Telegram bot
- Email (SMTP)
- Discord webhook
- Slack webhook

Triggered when:
- New job appears
- Job removed
- Stock status changes

---

## 🧪 Debugging Checklist

| Problem | Cause | Fix |
|------|------|-----|
Empty CSV | Page blocked | Solve CAPTCHA |
No elements | JS not loaded | Add WebDriverWait |
Works once only | Session lost | Use Chrome profile |
JSON empty | Data list empty | Print length(data) |

---

## 🚀 Final Project Vision

**CLI Tool**
```
python tracker.py --site tanitjobs --keyword react
```

Features:
- Scrape
- Detect changes
- Save CSV / JSON
- Notify
- Schedule

---

## 💖 Reminder
You are not "just scraping"  
You’re building **real automation engineering skills** 🔥

